import sys, os
import logging, time
import mysql.connector
from datetime   import datetime
from extensions import app, tools
from dotenv     import load_dotenv
from flask      import request, g as app_ctx

class PerformanceMonitor:
    def __init__(self) -> None:
        self.is_enabled = os.getenv('ENABLE_MONITORING') == "1"
        self.batch      = []
        self.max_batch  = 100
        self.batch_counter = 0
        
        self.setup()

    def gen_conn(self):
        DB_SERVER   = os.getenv('FLASK_MON_DB_SERVER')
        DB_USER     = os.getenv('FLASK_MON_DB_USER')
        DB_PASSWORD = os.getenv('FLASK_MON_DB_PASSWORD')
        DB_SCHEMA   = os.getenv('FLASK_MON_DB_SCHEMA')

        db_cfg = {
            'host'    : DB_SERVER,
            'user'    : DB_USER,
            'database': DB_SCHEMA,
            'password': DB_PASSWORD
        }
        logging.getLogger("mysql.connector").setLevel(logging.WARNING)
        return mysql.connector.connect(**db_cfg)

    def gen_curs(self):
        return self.conn.cursor()
    
    def close_conn_and_curs(self):
        self.curs.close()
        self.conn.close()

    def setup(self):
        tools.info(f'Performance Monitoring enabled: {self.is_enabled}')

        if self.is_enabled:
            load_dotenv()
            self.setup_db()
        else:
            return

    def setup_db(self):
        self.conn = self.gen_conn()
        self.curs = self.gen_curs()

    @app.before_request
    def logging_before(self):
        if self.is_enabled:
            app_ctx.start_time = time.perf_counter()
        else:
            return

    @app.after_request
    def logging_after(self, response):
        if self.is_enabled:
            total_time = time.perf_counter() - app_ctx.start_time
            time_in_ms = int(total_time * 1000)
            self.post_perf_data(
                **{
                    'method'     : request.method,
                    'endpoint'   : request.url_rule.rule,
                    'status_code': response.status_code,
                    'res_time'   : time_in_ms,
                }
            )
            return response
        else:
            return
        
    def _submit(self, *args, **kwargs):
        order = ['timestamp', 'method', 'endpoint', 'code', 'time']
        self.batch.append( ( [ kwargs[key] for key in order ] ) )

        if self.batch_counter == self.max_batch:
            self.multi_submit()

        return

    def submit(self, now: datetime, method: str, endpoint: str, code: int, time: int):
        self.batch.append((now, method, endpoint, code, time))

        if self.batch_counter == self.max_batch:
            self.multi_submit()
        
        return

    def multi_submit(self):
        self.info(f'{self.batch_counter} reached limit, submitting to performance DB.')
        insert_query = "INSERT INTO flask_perf (timestamp, method, endpoint, status_code, res_time) VALUES (%s,%s,%s,%s,%s)"

        self.curs.executemany(insert_query, self.batch)
        self.conn.commit()

        self.batch = []
        self.batch_counter = 0

    def post_perf_data(self, *args, **kwargs):
        self.batch_counter += 1
        now    = datetime.now()
        method = kwargs.get('method', None)
        rule   = kwargs.get('endpoint', None)
        code   = kwargs.get('status_code', None)
        time   = kwargs.get('res_time', None)

        try:
            self.submit(now, method, rule, code, time)
        except mysql.connector.errors.OperationalError as e:
            self.error('Connection to SQL performance database timed out, reconnecting...')
            self.close_conn_and_curs()
            self.setup_db()
            self.post_perf_data(**kwargs)

    def dispose(self):
        self.close_conn_and_curs()
        sys.exit(0)