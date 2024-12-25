import json
from sqlalchemy import delete
from models     import Grex_mon
from flask      import Blueprint, request
from extensions import tools, Response, db

grocer_routes = Blueprint('grocer_routes', __name__)

@grocer_routes.route('/grocer', methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def im_alive():
    resp = Response()

    tools.log_request(request)

    resp.set_msg('OK')
    resp.set_success()
    resp.set_data({'grocer': True})

    return tools._respond(request, **resp.serialize())