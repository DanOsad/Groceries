from models import Grex_mon
from datetime import datetime
from flask import Blueprint, request
from extensions import db, tools, Response
from sqlalchemy import or_, and_, func, case, delete

simba_single = Blueprint('simba_single', __name__)

@simba_single.route('/job', methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def job():
    resp = Response()

    if request.method == 'GET': # GET JOB
        tools.log_request(request)

        try:
            row_id = request.form.get('id', None)
            if row_id:
                job = Grex_mon.query.filter_by(id = row_id).first()
                if job:
                    resp.set_success()
                    resp.set_msg(f'Job {row_id} found')
                    resp.set_data(job.as_dict)
            else:
                resp.set_failure()
                resp.set_msg('ID not provided')
        except Exception as e:
                resp.set_failure()
                resp.set_msg(f'Could not find process {row_id} due to {e}, please check the ID you submitted')
                tools.debug_response(resp._msg, e)

        return tools._respond(request, **resp.serialize())
    
    if request.method == 'POST': # NEW JOB
        tools.log_request(request)
        try:
            val_fields = ['parent_id']
            bool_fields = ['is_multi_inst', 'is_alive', 'is_parent', 'is_jenkins']

            job = Grex_mon(
                **{
                    col: request.form.get(col, 'N/A') if col in val_fields else
                    (True if request.form.get(col, False) == "True" else False) if col in bool_fields else
                    request.form.get(col, None)
                    for col in Grex_mon().columns
                }
            )
            db.session.add(job)
            db.session.flush()
            db.session.commit()
            
            resp.set_success()
            resp.set_data(job.id)
            resp.set_msg(f'Job {job.id} updated')
        
        except Exception as e:
            resp.set_failure()
            resp.set_msg(f'Could not create job')
            tools.debug_response(resp._msg, e)

        return tools._respond(request, **resp.serialize())

    if request.method == 'PATCH': # UPDATE JOB
        tools.log_request(request)
        
        try:
            row_id = request.form.get('id', None)
            if row_id:
                bool_fields = ['is_alive', 'is_multi_inst', 'is_parent', 'is_jenkins']
                date_fields = ['q_time', 's_time', 'e_time']
                jid_fields  = ['job_id']
                
                Grex_mon.query.filter_by(id = row_id).update(
                    {
                        col: 
                            (request.form.get(col, False) == "True" if col in bool_fields
                            else datetime.strptime(request.form.get(col, None),'%a, %d %b %Y %H:%M:%S %Z') if col in date_fields and tools.validate_date(request.form.get(col, None)) ## Thu, 29 Jun 2023 10:46:13 GMT ## and isinstance(request.form.get(col), str)
                            else request.form.get(col, None))
                        for col in Grex_mon().columns if col in request.form
                    }
                )
                db.session.commit()

                resp.set_success()
                resp.set_msg(f'Job {row_id} updated')

        except Exception as e:
            resp.set_failure()
            resp.set_msg(f'Could not find job {row_id}')
            tools.debug_response(resp._msg, e)

        return tools._respond(request, **resp.serialize())
    
    if request.method == 'DELETE': # KILL PARENTS + CHILDREN
        tools.log_request(request)

        try:
            job_id = request.form.get('id', None)
            
            if job_id:
                job = Grex_mon.query.get(job_id)
                job.status = 'Killed'
                db.session.commit()

                resp.set_success()
                resp.set_msg(f'Killed job {job_id} in DB')
            else:
                resp.set_failure()
                resp.set_msg('No job id provided')

        except Exception as e:
            resp.set_failure()
            resp.set_msg(f'Could not kill job {job_id} due to {e}')
            tools.debug_response(resp._msg, e)

        return tools._respond(request, **resp.serialize())