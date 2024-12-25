import json
from sqlalchemy import delete
from models     import Grex_mon
from flask      import Blueprint, request
from extensions import tools, Response, db

order_queue_routes = Blueprint('order_queue_routes', __name__)

@order_queue_routes.route('/order_queue', methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def im_alive():
    resp = Response()

    tools.log_request(request)

    resp.set_msg('OK')
    resp.set_success()
    resp.set_data({'order_queue': True})

    return tools._respond(request, **resp.serialize())