import json
from sqlalchemy import delete
from models     import Grex_mon
from flask      import Blueprint, request
from extensions import tools, Response, db

simba_generic = Blueprint('simba_generic', __name__)

@simba_generic.route('/', methods=['GET'])
def hello():
    return 'Hello, world!', 200

@simba_generic.route('/is_alive', methods=['GET'])
def im_alive():
    resp = Response()

    tools.log_request(request)

    resp.set_msg('OK')
    resp.set_success()
    resp.set_data({'is_alive': True})

    return tools._respond(request, **resp.serialize())

#### DELETE ####
@simba_generic.route('/delete', methods=['DELETE'])
def delete_rows():
    resp = Response()

    if request.method == 'DELETE':
        tools.log_request(request)

        try:
            data = json.loads(request.json)
            del_list = data.get('del_list', [])

            del_list = [ int(item) if isinstance(item, str) else item for item in del_list ]

            if del_list:
                query = delete(Grex_mon).where(Grex_mon.id.in_(del_list))

                db.session.execute(query)
                db.session.commit()
                
                resp.set_success()
                resp.set_msg(f'Deleted rows {del_list}')
            
            else:
                resp.set_failure()
                resp.set_msg(f'No rows to delete')

        except Exception as e:
            resp.set_failure()
            resp.set_msg(f'/delete failed with del_list {del_list}')
            tools.debug_response(resp._msg, e)

        return tools._respond(request, **resp.serialize())