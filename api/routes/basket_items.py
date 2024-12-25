import json
from sqlalchemy import delete
from models     import Grex_mon
from flask      import Blueprint, request
from extensions import tools, Response, db

basket_item_routes = Blueprint('basket_item_routes', __name__)

@basket_item_routes.route('/basket_item', methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def im_alive():
    resp = Response()

    tools.log_request(request)

    resp.set_msg('OK')
    resp.set_success()
    resp.set_data({'basket_item': True})

    return tools._respond(request, **resp.serialize())