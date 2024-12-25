import json
from sqlalchemy import delete
from models     import Grex_mon
from flask      import Blueprint, request
from extensions import tools, Response, db

order_routes = Blueprint('order_routes', __name__)

@order_routes.route('/order', methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def im_alive():
    resp = Response()

    tools.log_request(request)

    resp.set_msg('OK')
    resp.set_success()
    resp.set_data({'order': True})

    return tools._respond(request, **resp.serialize())