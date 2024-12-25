import json
from sqlalchemy import and_
from models     import Grex_mon
from extensions import tools, db
from flask      import Blueprint, request
from datetime   import datetime, timedelta
from flask      import request, jsonify, render_template

simba_legacy = Blueprint('simba_legacy', __name__)

col_names = [
        'id',
        'uniq_jid',
        'job_id',
        'user',
        'project',
        'error_type',
        'args',
        'tb',
        'bc',
        'full_req',
        'h_name',
        'parent_id',
        'instructions',
        'timeout',
        'status',
        'data',
        'r_time',
        'c_time',
        'q_time',
        's_time',
        'e_time',
        'passed',
        'failed',
        'errors',
        'crashed',
        'grid_crashed',
        'total_bytes',
        'total_transactions',
        'total_cycles',
        'test_name',
        'maxvmem',
        'end_time',
        'start_time',
        'sim_time_ns',
        'run_time_sec',
        'sim_rate_hz',
        'trans_per_second',
        'gb_per_sec',
        'req_mem',
        'mem_diff',
        'mem_usage_diff_float',
        'test_location',
        'high_mem',
        'r_time_ns',
        'avg_mem',
        'regression_name',
        'srl',
        'test_id',
        'port_type',
        'ports',
        'dump',
        'trex_log',
        'sv_cmd',
        'tool_ver',
        'is_alive',
        'is_multi_inst',
        'last_alive_ping',
        'is_parent',
        'is_jenkins',
        'recheck'
        ]
    
@simba_legacy.route('/commands/<username>', methods=['GET', 'POST']) ## FOR GUI ##
def get_commands(username):
    if request.method in ['GET', 'POST']:
        # user = request.form.get('user', None)
        user=username

        if user:
            tools.info(f'GET /commands accessed from {request.remote_addr}')
            search_from = 500000
            limit = 10
            last_row = Grex_mon.query.order_by(Grex_mon.id.desc()).first().id
            jobs = Grex_mon.query.order_by(Grex_mon.id.desc())              \
                                 .filter(and_(                              \
                                    Grex_mon.user==user,                    \
                                    Grex_mon.id>=(last_row - search_from),  \
                                    Grex_mon.is_parent==True,               \
                                    Grex_mon.full_req!=None                 \
                                    )                                       \
                                 )                                          \
                                 .limit(limit)                              \
                                 .all()
            if jobs:
                jobs = [ job.serialize for job in jobs ]
                commands = [ job['full_req'] for job in jobs ]

                response = jsonify({'cmds': commands})
                response.headers.add('Access-Control-Allow-Origin', '*')

                return response, 200
        
        return jsonify({'success': False}), 400

@simba_legacy.route('/is_complete/<process_id>', methods=['GET'])
def is_child_complete(process_id):
    if request.method == 'GET':
        row = Grex_mon.query.get(process_id)
        if row:
            return jsonify(
                {
                    'success': True,
                    'status_code': 200,
                    'status': row.status,
                    'is_complete': True if row.status in ['Done', 'Completed', 'Passed', 'Failed', 'Crashed', 'GridCrashed'] else False
                }
            )
        else:
            return jsonify(
                {
                    'success': False,
                    'status_code': 400
                }
            )
@simba_legacy.route('/get_children/<parent_id>', methods=['GET'])
def get_parents_children(parent_id):
    resp_obj = {
        'msg'        : None,
        'data'       : None,
        'success'    : None,
        'status_code': None,
    }

    if request.method == 'GET':

        tools.info(f'/get_children GET accessed from {request.remote_addr}')

        try:

            if parent_id:
                
                jobs = Grex_mon.query.filter(and_(Grex_mon.id > parent_id, Grex_mon.parent_id == parent_id)).all()
                
                if jobs:

                    resp_obj['data']        = [ job.as_dict for job in jobs ]
                    resp_obj['msg']         = f'Found {len(resp_obj["data"])} jobs with parent_id {parent_id}'
                    resp_obj['success']     = True
                    resp_obj['status_code'] = 200

                    tools.info(resp_obj['msg'])
            
            else:

                resp_obj['msg']         = f'Parent id either invalid or not found'
                resp_obj['success']     = False
                resp_obj['status_code'] = 400

                tools.error(resp_obj['msg'])

            return resp_obj, resp_obj['status_code']

        except Exception as e:

            resp_obj['msg']         = f'Could not get jobs due to {e}, please check the parent_id you submitted'
            resp_obj['success']     = False
            resp_obj['status_code'] = 400

            tools.error(resp_obj['msg'])

            return resp_obj, resp_obj['status_code']

@simba_legacy.route('/all_complete/<parent_id>', methods=['GET'])
def all_children_complete(parent_id):
    if request.method == 'GET':
        children = Grex_mon.query.filter_by(parent_id = parent_id).all()
        # children = jsonify([i.serialize for i in children])
        for child in children:
            if child.status not in ['Passed', 'Failed', 'Crashed', 'GridCrashed', 'Completed', 'Done', 'completed', 'done']:
                return jsonify({'all_complete': False})
        return jsonify({'all_complete': True})

@simba_legacy.route('/grandfather_all_complete/<grandfather_id>', methods=['GET'])
def all_fathers_complete(grandfather_id):
    if request.method == 'GET':
        children = Grex_mon.query.filter(Grex_mon.id >= int(grandfather_id)).filter_by(parent_id = grandfather_id).all()
        for child in children:
            if child.status not in ['FINISH']:
                return jsonify({'all_complete': False})
        return jsonify({'all_complete': True})

@simba_legacy.route('/host/<h_name>', methods=['GET'])
def get_all_host_jobs(h_name):
    if request.method == 'GET':
        host_jobs = Grex_mon.query.filter_by(h_name = h_name).all()
        return render_template('./jobs.html', records=host_jobs, col_names = col_names)

@simba_legacy.route('/status/<status>', methods=['GET'])
def get_all_status_jobs(status):
    if request.method == 'GET':
        status_jobs = Grex_mon.query.filter_by(status = status).all()
        return render_template('./jobs.html', records = status_jobs, col_names = col_names)

@simba_legacy.route('/create_children', methods=['GET','POST'])
def gen_children():
    if request.method == 'POST':
        tools.info(f'/create_children POST accessed by {request.remote_addr}')
        try:
            rows = dict()

            data = json.loads(request.json)

            parent_id = data.get('parent_id', None)
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
                    'test_name' : child['test_name'] if 'GridTestAlias' not in child else child['GridTestAlias'],
                    'trex_log'  : child['trex_log'] if 'GridTestAlias' not in child else child['Paths']['SimLogPath']
                }

                job = Grex_mon( **{**child_job, **generic_data} )
                
                db.session.add(job)
                db.session.flush()
                
                rows[int(child['TestIDX'])] = job.id
            
            db.session.commit()

            # ################### GET ROW IDS ###################
            # jobs = Grex_mon.query.filter(Grex_mon.id>parent_id).filter_by(parent_id=parent_id).all()
            
            # if jobs:
            #     for child in child_objs:
            #         for job in [j.serialize for j in jobs]:
            #             if job['test_name'] == child['GridTestAlias']:
            #                 rows[child['TestIDX']] = job['id']
            #             # else:
            #             #     tools.error(f"Job not found for TestIDX {child['TestIDX']}")

            #     tools.info(f'Added new rows {rows}')
                
            if rows:
                return {
                        'rows'        : rows,
                        'text'        : f'Rows created for parend {parent_id}',
                        'success'     : True,
                        'created'     : True,
                        'status_code' : 200
                    }, 200
            
            else:
                tools.error(f'Unable to fetch newly created rows for parent {parent_id}')
                return {
                    'rows'       : None,
                    'success'    : False,
                    'text'       : 'Unable to fetch newly created rows',
                    'created'    : False,
                    'status_code': 400
                }, 400
        
        except Exception as e:
            tools.error('Unable to post new job, please check submitted fields for errors')
            tools.error(e)
            
            return {
                    'row_id'     : None,
                    'success'    : False,
                    'text'       : 'Unable to create new rows',
                    'created'    : False,
                    'status_code': 400
                }, 400

@simba_legacy.route('/new_job2', methods=['POST'])
def new_proc():
    if request.method == 'POST':
        tools.info('/new_job2 POST accessed')
        try:
            val_fields = ['parent_id']
            bool_fields = ['is_multi_inst', 'is_alive', 'is_parent', 'is_jenkins']
            # rate_hash = {
            #     'sim_time_ns': '38,201,266.000000075', 
            #     'run_time_sec': '5,756.6900000000005', 
            #     'sim_rate_hz': ''
            # }
            job = Grex_mon(
                **{
                    col: request.form.get(col, 'N/A') if col in val_fields else
                    (True if request.form.get(col, False) == "True" else False) if col in bool_fields else
                    request.form.get(col, None)
                    for col in col_names
                }
            )
            db.session.add(job)
            db.session.commit()
            tools.info(f'Added new job ID# {job.id}')
            return str(job.id), 201
        except Exception as e:
            tools.error('Unable to post new job, please check submitted fields for errors')
            tools.error(e)
            return {
                    'row_id'     : None,
                    'success'    : False,
                    'text'       : 'Unable to create new row',
                    'created'    : False,
                    'status_code': 400
                }, 400

@simba_legacy.route('/new_job', methods=['POST'])
def new_process():
    if request.method == 'POST':
        tools.info('/new_job POST accessed')
        try:
            job = Grex_mon(
                user            = request.form.get('user', None),
                project         = request.form.get('project', None),
                tb              = request.form.get('tb', None),
                bc              = request.form.get('bc', None),
                full_req        = request.form.get('full_req', None),
                h_name          = request.form.get('h_name', None),
                parent_id       = request.form.get('parent_id', 'N/A'),
                c_time          = request.form.get('c_time', None),
                q_time          = request.form.get('q_time', None),
                s_time          = request.form.get('s_time', None),
                e_time          = request.form.get('e_time', None),
                job_id          = request.form.get('job_id', None),
                uniq_jid        = request.form.get('uniq_jid', None),
                instructions    = request.form.get('instructions', None),
                timeout         = request.form.get('timeout', None),
                status          = request.form.get('status', None),
                passed          = request.form.get('passed', None),
                failed          = request.form.get('failed', None),
                crashed         = request.form.get('crashed', None),
                grid_crashed    = request.form.get('grid_crashed', None),
                errors          = request.form.get('errors', None),
                error_type      = request.form.get('error_type', None),
                data            = request.form.get('data', None),
                args            = request.form.get('args', None),
                trex_log        = request.form.get('trex_log', None),
                test_name       = request.form.get('test_name', None),
                req_mem         = request.form.get('req_mem', None),
                maxvmem         = request.form.get('maxvmem', None),
                mem_diff        = request.form.get('mem_diff', None),
                regression_name = request.form.get('regression_name', None),
                dump            = request.form.get('dump', None),
                sim_time_ns     = request.form.get('sim_time_ns', None),
                run_time_sec    = request.form.get('run_time_sec', None),
                sim_rate_hz     = request.form.get('sim_rate_hz', None),
                sv_cmd          = request.form.get('sv_cmd', None),
                tool_ver        = request.form.get('tool_ver', None),
                is_alive        = True if request.form.get('is_alive', False) == "True" else False,
                is_multi_inst   = True if request.form.get('is_multi_inst', False) == "True" else False,
                last_alive_ping = request.form.get('last_alive_ping', None),
                is_parent       = True if request.form.get('is_parent', False) == "True" else False,
                is_jenkins      = True if request.form.get('is_jenkins', False) == "True" else False,
                recheck         = request.form.get('recheck', None)
            )

            db.session.add(job)
            db.session.commit()
            tools.info(f'Added new job ID# {job.id}')
            return str(job.id), 201
        except Exception as e:
            tools.error('Unable to post new job, please check submitted fields for errors')
            tools.error(e)
            return 'Unable to post new job, please check submitted fields for errors', 400

@simba_legacy.route('/update_job/<process_id>', methods=['PATCH'])
def update_job_new(process_id):
    if request.method == 'PATCH':
        tools.info(f'/update_job PATCH accessed with job ID# {process_id}')
        try:
            bool_fields = ['is_alive', 'is_multi_inst', 'is_parent', 'is_jenkins']
            date_fields = ['q_time', 's_time', 'e_time']
            Grex_mon.query.filter_by(id = process_id).update(
                {
                    col: request.form.get(col) if col not in bool_fields else request.form.get(col, False) == "True" for col in col_names if col in request.form
                }
            )
            db.session.commit()
            tools.info(f'Process {process_id} updated')
            return f'Process {process_id} updated', 201
        except Exception as e:
            # tools.error(e) 
            tools.error(f'Could not find process {process_id} due to {e}, please check the ID you submitted')
            return f'Could not find process {process_id}, please check the ID you submitted', 400
        
@simba_legacy.route('/update_job2/<process_id>', methods=['PATCH'])
def update_job_new2(process_id):
    if request.method == 'PATCH':
        tools.info(f'/update_job2 PATCH accessed with job ID# {process_id}')
        try:
            bool_fields = ['is_alive', 'is_multi_inst', 'is_parent', 'is_jenkins']
            date_fields = ['q_time', 's_time', 'e_time']
            jid_fields  = ['job_id']
            Grex_mon.query.filter_by(id = process_id).update(
            # Grex_mon.query.get(process_id).update(
                {
                    # **{
                        col: 
                            (request.form.get(col, False) == "True" if col in bool_fields
                            else datetime.strptime(request.form.get(col, None),'%a, %d %b %Y %H:%M:%S %Z') if col in date_fields and validate_date(request.form.get(col, None)) ## Thu, 29 Jun 2023 10:46:13 GMT ## and isinstance(request.form.get(col), str)
                            # else request.form.get('uniq_jid').split('_')[0] if 'uniq_jid' in request.form and request.form.get('uniq_jid', None) is not None and '_' in request.form.get('uniq_jid', None)
                            else request.form.get(col, None))
                        for col in col_names if col in request.form
                        # for col in request.form
                    # },
                    # 'job_id': request.form.get('uniq_jid', None).split('_')[0] if 'uniq_jid' in request.form and request.form.get('uniq_jid', None) is not None and '_' in request.form.get('uniq_jid', None) else None
                }
            )
            db.session.commit()
            # if request.form.get('status', None) == 'Failed': tools.info(f'Process {process_id} failed: {request.form}')
            tools.info(f'Process {process_id} updated')
            # return f'Process {process_id} updated', 201
            return {
                'row_id'     : process_id,
                'success'    : True,
                'text'       : f'Process {process_id} updated',
                'updated'    : True,
                'status_code': 201
            }, 201
        except Exception as e:
            # tools.error(e) 
            tools.error(f'Could not find process {process_id} due to {e}, please check the ID you submitted')
            # return f'Could not find process {process_id}, please check the ID you submitted', 400
        return {
                'row_id'     : process_id,
                'success'    : False,
                'text'       : f'Process {process_id} failed to update',
                'updated'    : False,
                'status_code': 400,
                'error_msg'  : e
            }, 400
        
def validate_date(date_text):
        try:
            datetime.strptime(date_text,'%a, %d %b %Y %H:%M:%S %Z')
            return True
        except:
            return False

@simba_legacy.route('/update_parent', methods = ['POST'])
def update_father2():
    if request.method == 'POST':
        try:
            parent_id     = request.form.get('parent_id', None)
            parent_status = request.form.get('parent_status', None)
            is_multi_inst = request.form.get('is_multi_inst', False) == "True"
            is_alive      = request.form.get('is_alive', False) == "True"
            # jobnumber     = request.form.get('jobnumber', None)
            # is_parent     = request.form.get('is_parent', False) == "True"
            tools.info(f'/update_parent POST accessed with job ID# {parent_id}')


            statuses = {'passed': 0, 'failed': 0, 'crashed': 0, 'grid_crashed': 0}
            
            parent = Grex_mon.query.filter_by(id = parent_id)
            # parent_dict = { i.serialize for i in parent }
            children = Grex_mon.query.filter(Grex_mon.id >= int(parent_id)).filter_by(parent_id = parent_id).all()
            
            for child in children:
                status = child.status
                recheck = child.recheck
                if status in ['Failed', 'RTLError']:
                    statuses['failed'] += 1
                elif status in ['Passed']:
                    statuses['passed'] += 1
                elif status in ['Crashed']:
                    if (recheck and recheck == 'GridCrashed'):
                        statuses['grid_crashed'] += 1
                    elif (recheck and recheck != status and recheck in ['Passed', 'Failed']):
                        statuses[recheck.lower()] += 1
                    else:
                        statuses['crashed'] += 1

            tools.debug(f'Parent {parent_id} updated status counts are {statuses}')

            parent.update(
                {
                    'status'         : parent_status,
                    'is_alive'       : is_alive,
                    'is_multi_inst'  : is_multi_inst, 
                    'last_alive_ping': datetime.now(),
                    # 'job_id'         : jobnumber,
                    # 'status'         : parent_dict['status'] if not parent_status else parent_status,
                    # 'is_alive'       : parent_dict['is_alive'] if not is_alive else is_alive,
                    # 'is_multi_inst'  : parent_dict['is_multi_inst'] if not is_multi_inst else is_multi_inst, 
                    # 'last_alive_ping': parent_dict['last_alive_ping'] if not is_alive else datetime.now(),
                    **statuses
                }
            )
            db.session.commit()

            tools.info(f'Parent {parent_id} updated')
            return {'success': True}, 200
        except Exception as e:
            tools.error(f'Could not find parent {parent_id} due to {e}, please check the ID you submitted')
            return {'success': False}, 400

@simba_legacy.route('/recheck_parent/<parent_id>', methods=['GET','POST'])
def update_parent_after_recheck(parent_id):
    if request.method == 'POST':
        try:
            tools.info(f'/recheck_parent POST accessed with job ID# {parent_id}')

            statuses = {'passed': 0, 'failed': 0, 'crashed': 0, 'grid_crashed': 0}
            
            parent = Grex_mon.query.filter_by(id = parent_id)
            children = Grex_mon.query.filter(Grex_mon.id >= int(parent_id)).filter_by(parent_id = parent_id).all()
            
            for child in children:
                status = child.status
                recheck = child.recheck
                if status in ['Failed', 'RTLError']:
                    statuses['failed'] += 1
                elif status in ['Passed']:
                    statuses['passed'] += 1
                # elif status in ['Crashed'] and (recheck is not None and recheck == status):
                #     statuses['crashed'] += 1
                # elif status in ['GridCrashed']:
                #     statuses['grid_crashed'] += 1
                elif status in ['Crashed']:
                    if (recheck and recheck == 'GridCrashed'):
                        statuses['grid_crashed'] += 1
                    elif (recheck and recheck != status and recheck in ['Passed', 'Failed']):
                        statuses[recheck.lower()] += 1
                    else:
                        statuses['crashed'] += 1

            tools.debug(f'Parent {parent_id} updated status counts are {statuses}')

            parent.update( { **statuses } )
            db.session.commit()

            tools.info(f'Parent {parent_id} updated')
            
            return {'success': True}, 200
        except Exception as e:
            tools.error(f'Could not find parent {parent_id} due to {e}, please check the ID you submitted')
            
            return {'success': False}, 400

@simba_legacy.route('/get_job/<process_id>', methods=['GET'])
def get_process(process_id):
    if request.method == 'GET':
        tools.info(f'/get_job GET accessed with job ID {process_id}')
        try:
            job = Grex_mon.query.filter_by(id = process_id)
            tools.info(f'Job {process_id} found')
            return jsonify([i.serialize for i in job]), 200
        except Exception as e:
            tools.error(f'Could not find process {process_id} due to {e}, please check the ID you submitted')
            return {'success': False}, 400

@simba_legacy.route('/is_parent_alive/<process_id>', methods=['GET'])
def get_parent_is_alive(process_id):
    if request.method == 'GET':
        tools.info(f'/is_parent_alive GET accessed with job ID {process_id}')
        try:
            job = Grex_mon.query.filter_by(id = process_id)
            job = jsonify([i.serialize for i in job])
            tools.info(f'Job {process_id} found')
            tools.info(job)
            return jsonify({
                'success': True,
                'is_alive': job['is_alive'] and job['last_alive_ping'] >= datetime.now() - timedelta(minutes=30)
            }), 200
        except Exception as e:
            tools.error(f'Could not find process {process_id} due to {e}, please check the ID you submitted')
            return {'success': False}, 400

@simba_legacy.route('/job/<uniq_jid>', methods=['GET', 'POST'])
def job_uniq_jid(uniq_jid):
    if request.method == 'GET':
        tools.info(f'/job GET accessed with uniq_jid# {uniq_jid}')
        job = Grex_mon.query.filter_by(uniq_jid = uniq_jid)
        if job:
            tools.info(f'Job {uniq_jid} found using uniq_jid method')
            return jsonify([i.serialize for i in job]), 200
        else:
            return f'Job with uniq_jid {uniq_jid} not found', 404
    if request.method == 'POST':
        tools.info(f'/job POST accessed with uniq_jid# {uniq_jid}')
        try:
            Grex_mon.query.filter_by(uniq_jid = uniq_jid).update({col: request.form.get(col) for col in col_names if col in request.form})
            db.session.commit()
            tools.info(f'UNIQ_JID {uniq_jid} updated')
            return f'UNIQ_JID {uniq_jid} updated', 201
        except:
            tools.error(f'Could not find UNIQ_JID {uniq_jid}, please check the ID you submitted')
            return f'Could not find UNIQ_JID {uniq_jid}, please check the ID you submitted', 400

@simba_legacy.route('/last_day_crashed', methods=['GET'])
def get_last_day_crashed():
    if request.method == 'GET':
        tools.info(f'/last_day_crashed GET accessed')
        
        one_day_ago = datetime.now() - timedelta(days=1)
        last_row    = Grex_mon.query.order_by(Grex_mon.id.desc()).first()
        max_id      = last_row.id
        max_rows    = 200000
        search_from = max_id - max_rows

        jobs = Grex_mon.query.filter(Grex_mon.id >= search_from).filter(Grex_mon.c_time >= one_day_ago).all()
        serialized_jobs = [i.serialize for i in jobs]
        crashed_jobs = list(filter(lambda job: job['status'] == 'Crashed', serialized_jobs))
        tools.info(f'/last_day_crash found {len(crashed_jobs)} crashed jobs')
        parent_list = list(set([ job['parent_id'] for job in crashed_jobs ]))
        
        if jobs:
            return {
                'num_crashed_jobs': len(crashed_jobs),
                'parents': parent_list,
                'success': True,
                'date_from': one_day_ago,
                'logs': [(job['id'], job['trex_log']) for job in serialized_jobs if (job['status'] in ['Crashed'] and not job['recheck'])]
                }
        else:
            return {
                'success': False,
                'msg': f'Could not find rows from {one_day_ago}'
            }

@simba_legacy.route('/kill/<user>', methods=['PUT'])
def db_cleanup(user):
    if request.method == 'PUT':
        tools.info(f'/kill PUT accessed with user {user}')
        changed_ids = []
        user_jobs = Grex_mon.query.filter_by(user=user).all()
        all_results = [i.serialize for i in user_jobs]
        if len(all_results) < 1:
            tools.error(f'No jobs found for user {user}')
            return 'No jobs found for user {}'.format(user)
        i = -1
        last_job = all_results[i]
        while last_job['status'] == 'Killed':
            i -= 1
            last_job = all_results[i]
        changed_ids.append(last_job['parent_id'])
        parent = Grex_mon.query.get(last_job['parent_id'])
        parent.status = 'Killed'
        db.session.add(parent)
        children = Grex_mon.query.filter_by(parent_id = last_job['parent_id']).all()
        for child in children:
            changed_ids.append(child.id)
            child.status = 'Killed'
            db.session.add(child)
        db.session.commit()
        tools.info(f'Rows {",".join(changed_ids)} have been killed')
        return f'The following DB rows have been killed: {changed_ids}'

@simba_legacy.route('/killed/<process_id>', methods=['PUT'])
def kill_process(process_id):
    if request.method == 'PUT':
        tools.info(f'/killed PUT accessed with process_id {process_id}')
        try:
            job         = Grex_mon.query.get(process_id)
            job.status  = 'Killed'

            db.session.add(job)
            db.session.commit()

            tools.info(f'Job {process_id} was successfully killed')
            return f'Job {process_id} was successfully killed', 200
        except:
            tools.error(f'Could not find process {process_id}, please check the ID you submitted')
            return f'Could not find process {process_id}, please check the ID you submitted', 400

@simba_legacy.route('/kill_parent/<process_id>', methods=['PUT'])
def kill_parent(process_id):
    if request.method == 'PUT':
        tools.info(f'/kill_parent PUT accessed with process_id {process_id}')
        try:
            changed_ids         = list()
            parent_job          = Grex_mon.query.get(process_id)
            parent_job.status   = 'Killed'
            children            = Grex_mon.query.filter(Grex_mon.id >= process_id).filter_by(parent_id = process_id).all()

            for child in children:
                changed_ids.append(str(child.id))
                child.status = 'Killed'
                db.session.add(child)

            db.session.commit()
            
            tools.info(f'Rows {",".join(changed_ids)} have been killed')
            return f'The following DB rows have been killed: {changed_ids}', 201
        except:
            tools.error(f'Could not find process {process_id}, please check the ID you submitted')
            return f'Could not find process {process_id}, please check the ID you submitted', 400

@simba_legacy.route('/get_pilot_stats/<date>', methods=['GET'])
def stats(date):
    if request.method == 'GET':
        timestamp   = datetime.strptime(date, '%Y-%m-%d')
        runs        = [i.serialize for i in Grex_mon.query.filter(Grex_mon.parent_id == 'N/A').filter(Grex_mon.q_time > timestamp)]
        
        if runs: return json.dumps([{key: val for key, val in run.items() for run in runs if key in ['status', 'bc', 'user', 'project', 'passed', 'failed', 'crashed']} for run in runs if run['status'] in ['FINISH', 'DoneFIX', 'CRASHED']])
        
        return f"Failed to find Simba runs after {date}"

@simba_legacy.route('/find_mem_combs', methods=['GET'])
def find_combs():
    if request.method == 'GET':
        project = request.form.get('project')
        tb = request.form.get('tb')
        bc = request.form.get('bc')

        filter_data = {'tb': tb, 'bc': bc, 'project': project}
        filter_data = {k:v for k,v in filter_data.items() if v}
        rows = Grex_mon.query.filter_by(**filter_data).all()

        def filter_mems(item):
            return item != 'N/A' or item is not None

        tools.info('/find_mem_combs GET accessed')

        if rows:
            tools.info(f'/find_mem_combs found combinations for TB:{tb} & BC:{bc}')
            mems = []
            for row in [i.serialize for i in rows]:
                if row['maxvmem'] != 'N/A' and row['maxvmem'] != None:
                    mems.append(float(row['maxvmem']))
            return jsonify(mems)
        else:
            tools.error(f'/find_mem_combs found NO combinations for TB:{tb} & BC:{bc}')
            return jsonify([])

@simba_legacy.route('/get_all_combos', methods=['GET'])
def get_all_mems():
    if request.method == 'GET':
        tools.info("/get_all_combos GET accessed")

        mems = {
            'alon': set(),
            'arbel': set()
        }

        jobs = Grex_mon.query.all()

        for job in jobs:
            if job.project == 'alon':
                mems['alon'].add((job.tb, job.bc))
            elif job.project == 'arbel':
                mems['arbel'].add((job.tb, job.bc))

        mems = {k: list(v) for k,v in mems.items()}
        # mems['alon'] = list(mems['alon'])
        # mems['arbel'] = list(mems['arbel'])

        return jsonify(mems), 201

@simba_legacy.route('/build_view', methods=['GET'])
def build_single_view():
    if request.method == 'GET':
        tb = request.form.get('tb')
        bc = request.form.get('bc')
        project = request.form.get('project')
        test_name = request.form.get('test_name')
        test_modes = request.form.get('test_modes')

        filter_data = {'tb': tb, 'bc': bc, 'project': project}
        filter_data = {k:v for k,v in filter_data.items() if v}
        rows = Grex_mon.query.filter_by(**filter_data).all()

        response = []

        for row in [i.serialize for i in rows]:
            if (row['maxvmem'] != 'N/A' and row['maxvmem'] is not None) and (row['test_name'] != 'N/A' and row['test_name'] is not None):
                response.append({
                    'tb': row['tb'],
                    'bc': row['bc'],
                    'project': row['project'],
                    'test_name': row['test_name'],
                    'maxvmem': row['maxvmem']
                })

        return jsonify(response)