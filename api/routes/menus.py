import json
from sqlalchemy import delete
from models     import Grex_mon
from flask      import Blueprint, request
from extensions import tools, Response, db

menu_routes = Blueprint('menu_routes', __name__)

@menu_routes.route('/menu', methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def im_alive():
    resp = Response()

    tools.log_request(request)

    resp.set_msg('OK')
    resp.set_success()
    resp.set_data({'menu': True})

    return tools._respond(request, **resp.serialize())