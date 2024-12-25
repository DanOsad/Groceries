import os, logging
from flask import Flask
from pathlib import Path
from copy import deepcopy
from dotenv import load_dotenv
from datetime import datetime
from .constants import HTTPStatusCode
from flask_sqlalchemy import SQLAlchemy
from .response import Response, Success, Failure

app = Flask(__name__)

load_dotenv()

DB_SERVER   = os.getenv('GROCERIES_SERVER')
DB_USER     = os.getenv('GROCERIES_USER')
DB_PASSWORD = os.getenv('GROCERIES_PASSWORD')
DB_SCHEMA   = os.getenv('GROCERIES_SCHEMA')

app.config['SQLALCHEMY_DATABASE_URI']           = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_SERVER}/{DB_SCHEMA}'
app.config['SQLALCHEMY_TRACK_NOTIFICATIONS']    = False
app.config['SQLALCHEMY_RECORD_QUERIES']         = False
app.config['SQLALCHEMY_ECHO']                   = False

db = SQLAlchemy(app)
# db = SQLAlchemy(app)
# db.session.begin()
# db.session.begin(subtransactions=True)

class FlaskApp:
    def __init__(self) -> None:
        self.setup()

    def setup(self):
        self.config_logger()
        self.info(f'Flask server started on {os.getenv("HOSTNAME")}')

    def config_logger(self):
        if os.getenv('LOG_DIR'):
            log_path = os.path.join(os.getenv('LOG_DIR'), 'flask.log')
        else:
            curr_path = os.path.abspath(__file__)
            path_obj  = Path(curr_path)
            directory = path_obj.parent.parent
            log_path  = directory / 'logs/flask.log'

        logging.basicConfig(
            format   ='%(asctime)s %(levelname)s: %(message)s',
            level    = logging.DEBUG,
            filename = log_path
            )
        log = logging.getLogger()

        self.info  = log.info
        self.error = log.error
        self.warn  = log.warning
        self.debug = log.debug

        self.debug(f'Logger configured to {log_path}')

    def validate_date(date_text):
        try:
            datetime.strptime(date_text,'%a, %d %b %Y %H:%M:%S %Z')
            return True
        except:
            return False

    def resp_obj(self):
        resp_obj = {
                'success'    : False,
                'status_code': HTTPStatusCode.NOT_FOUND.value
            }
        
        return deepcopy(resp_obj)
    
    def success(self, *args, **kwargs):
        resp_obj = self.resp_obj()
        resp_obj.update(
            {
                'success': True,
                'status_code': HTTPStatusCode.OK.value,
                **kwargs
            }
        )

        if kwargs['msg']:
            self.info(kwargs['msg'])

        return resp_obj

    def failure(self, *args, **kwargs):
        resp_obj = self.resp_obj()
        resp_obj.update(
            {
                'success': False,
                'status_code': HTTPStatusCode.NOT_FOUND.value,
                **kwargs
            }
        )

        if kwargs['msg']:
            self.error(kwargs['msg'])

        return resp_obj
    
    def _respond(self, request, **kwargs):
        msg     = kwargs.pop('msg', str())
        data    = kwargs.pop('data', dict())
        # request = kwargs.pop('request', None)
        success = kwargs.pop('success', False)

        if not request:
            msg  = 'Request body not found'
            resp = self.failure(**{'msg': msg})
        if success and request:
            msg  = f'{request.method} {request.url_rule.rule} succeeded : {msg}'
            if data:
                resp = self.success(**{'msg': msg, 'data': data})
            else:
                resp = self.success(**{'msg': msg})
        elif not success and request:
            msg  = f'{request.method} {request.url_rule.rule} failed : {msg}'
            resp = self.failure(**{'msg': msg})

        return resp, resp['status_code']

    def respond(self, request, msg, data, success):
        if success :
            msg  = f'{request.method} {request.url_rule.rule} succeeded : {msg}'
            if data:
                resp = self.success(**{'msg': msg, 'data': data})
            else:
                resp = self.success(**{'msg': msg})
        else:
            msg  = f'{request.method} {request.url_rule.rule} failed : {msg}'
            resp = self.failure(**{'msg': msg})

        return resp, resp['status_code']

    def log_request(self, request):
        self.info(f'{request.method} {request.url_rule.rule} accessed by {request.remote_addr}')

    def debug_response(self, msg: str, error: str):
        self.debug(msg)
        self.debug(error)

# class Response:
#     def __init__(self):
#         self._msg     = str()
#         self._data    = dict()
#         self._success = bool(False)

#     def set_success(self):
#         self._success = True

#     def set_failure(self):
#         self._success = False

#     def set_msg(self, msg):
#         self._msg = msg

#     def set_data(self, data):
#         self._data = data

#     def serialize(self):
#         return {
#             'msg'    : self._msg,
#             'data'   : self._data,
#             'success': self._success,
#         }