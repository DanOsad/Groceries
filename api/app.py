__VERSION__ = "1.1.0"

import sys
sys.dont_write_bytecode = True

import waitress
import werkzeug
import werkzeug.serving
# from werkzeug._reloader import run_with_reloader
from flask      import request, g as app_ctx
from extensions import app, FlaskApp#, flask_app#, perf_mon, PerformanceMonitor
from routes     import *

#### BLUEPRINTS ####
app.register_blueprint(basket_routes)
app.register_blueprint(basket_item_routes)
app.register_blueprint(customer_routes)
app.register_blueprint(grocer_routes)
app.register_blueprint(menu_routes)
app.register_blueprint(order_queue_routes)
app.register_blueprint(order_routes)
app.register_blueprint(single_item_routes)
app.register_blueprint(single_weighted_item_routes)

#### PERFORMANCE MONITOR ####
# perf = PerformanceMonitor()

#### RUN SERVER ####
# @werkzeug.serving.run_with_reloader
# @werkzeug._reloader.run_with_reloader
# def run_server():
#     app.debug = True
    # werkzeug.serving.run_simple('localhost', 5000, app, use_reloader=True)
    # waitress.serve(app, listen='0.0.0.0:5000', threads=16)
app.debug = True
server_config = {
    'hostname': "0.0.0.0",
    'port': 5000,
    'application': app,
    'use_reloader': True
}
werkzeug.serving.run_simple(
    hostname = "0.0.0.0",
    port = 5000,
    application = app,
    use_reloader = True
)
# if __name__ == "__main__":
    # run_server()
# werkzeug._reloader.run_with_reloader(run_server())