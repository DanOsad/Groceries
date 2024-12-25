import json
from models import Grex_mon
from flask import request, Blueprint
from extensions import db, tools, Response
from sqlalchemy import or_, and_, func, case, delete

simba_batch  = Blueprint('simba_batch', __name__)

@simba_batch.route('/batch', methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def parents():
    resp = Response()

    if request.method == 'GET': # GET CHILDREN
        tools.log_request(request)

        try:
            
            parent_id = request.form.get('id', None)
            
            if parent_id:
                
                jobs = Grex_mon.query.filter(and_(Grex_mon.id > parent_id, Grex_mon.parent_id == parent_id)).all()
                
                if jobs:
                    resp.set_success()
                    resp.set_msg(f'Found {len(data)} jobs with parent_id {parent_id}')
                    resp.set_data([ job.as_dict for job in jobs ])
            else:
                resp.set_failure()
                resp.set_msg('ID not provided')

        except Exception as e:
            resp.set_failure()
            resp.set_msg(f'Could not find jobs with parent_id {parent_id}')
            tools.debug_response(resp._msg, e)

        return tools._respond(request, **resp.serialize())
    
    if request.method == 'POST': # CREATE CHILDREN
        tools.log_request(request)

        try:
            rows = dict()

            data = json.loads(request.json)

            parent_id = data.get('id', 'N/A')
            val_fields  = ['parent_id']
            bool_fields = ['is_multi_inst', 'is_alive', 'is_parent', 'is_jenkins']
            
            generic_data = {
                col: data.get(col, 'N/A') if col in val_fields else
                (True if data.get(col, False) == "True" else False) if col in bool_fields else
                data.get(col, None)
                for col in data if col not in ['tests']
            }

            child_objs = data.get('tests')
            
            for child in child_objs:
                child_job = {
                    # 'idx'       : child['TestIDX'],
                    'test_name' : child['test_name'],
                    'trex_log'  : child['trex_log']
                }

                job = Grex_mon( **{**child_job, **generic_data} )
                
                db.session.add(job)
                db.session.flush()
                
                rows[int(child['TestIDX'])] = job.id
            
            db.session.commit()

            resp.set_success()
            resp.set_data(rows)
            resp.set_msg(f'{len(rows)} created for parent {parent_id}')

        except Exception as e:
            resp.set_failure()
            resp.set_msg(f'Unable to create new rows for parent {parent_id}')
            tools.debug_response(resp._msg, e)

        return tools._respond(request, **resp.serialize())

    if request.method == 'DELETE': # KILL PARENTS + CHILDREN
        tools.log_request(request)

        try:
            parent_id = request.form.get('parent_id', None)
            
            if parent_id:
                Grex_mon.query.filter(or_(Grex_mon.id == parent_id, and_(Grex_mon.id > parent_id, Grex_mon.parent_id == parent_id))).update({'status': 'Killed'})
                db.session.commit()

                resp.set_success()
                resp.set_msg(f'Killed parent {parent_id} and all children in DB')
            else:
                resp.set_msg(f'No parent id provided')

        except Exception as e:
            resp.set_failure()
            resp.set_msg(f'Could not kill job {parent_id}')
            tools.debug_response(resp._msg, e)

        return tools._respond(request, **resp.serialize())