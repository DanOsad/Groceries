import json
from sqlalchemy import delete
from models     import Grex_mon
from flask      import Blueprint, request
from extensions import tools, Response, db

single_weighted_item_routes = Blueprint('single_weighted_item_routes', __name__)

@single_weighted_item_routes.route('/single_weighted_item', methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def im_alive():
    resp = Response()

    tools.log_request(request)

    resp.set_msg('OK')
    resp.set_success()
    resp.set_data({'single_weighted_item': True})

    return tools._respond(request, **resp.serialize())