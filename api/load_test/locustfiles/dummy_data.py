import time, json, os
from datetime import datetime
import random, string

def gen_test_list():
    test_list = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test_data.json')))

    return random.sample(test_list, k=random.randint(20,100))

def gen_random_job_id():
    return random.randint(900000,999999)

def gen_random_path(user, project):
    dir = ''.join(random.choice(string.ascii_lowercase) for i in range(10))
    return f'/projects/{project}/work/{user}/dir/simba.log'

def gen_random_status():
    statuses = ['running', 'failed', 'passed', 'completed', 'pending', 'killed', 'crashed']
    return random.choice(statuses)

def gen_random_user():
    users   = ['dano', 'dory', 'lironi', 'rony', 'stasy', 'zach', 'zorro']
    return random.choice(users)

def gen_random_tb():
    tbs     = ['alon_ver', 'arbel_ver', 'cms_ver', 'hiu_ver', 'css_ver', 'pfe_ver', 'dpu_ver']
    return random.choice(tbs)

def gen_random_host():
    hosts   = [f'lx{x}' for x in range(100,212)]
    return random.choice(hosts)

def gen_random_project():
    projects = ['alon', 'arbel']
    return random.choice(projects)

def gen_random_bool():
    bools   = [True, False]
    return random.choice(bools)

def gen_random_tool_ver():
    tool_vers = ['1.96', '1.93', '1.95']
    return random.choice(tool_vers)

def create_parent_data():
    return {
        # 'user'        : gen_random_user(),
        'user'        : 'dummy_user',
        'project'     : gen_random_project(),
        'tb'          : gen_random_tb(),
        'bc'          : gen_random_tb(),
        'is_jenkins'  : gen_random_bool(),
        'is_alive'    : gen_random_bool(),
        'status'      : gen_random_status(),
        'tool_ver'    : gen_random_tool_ver(),
        'h_name'      : gen_random_host(),
        'job_id'      : gen_random_job_id(),
        'trex_log'    : gen_random_path(random.choice(gen_random_user()), random.choice(gen_random_project())),
        'last_alive'  : datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S'),
        'c_time'      : datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S'),
        'q_time'      : datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S'),
        's_time'      : datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S'),
        'is_parent'   : True,
        'instructions': '1', 
        'timeout'     : 0, 
    }

def create_children_data():
    return {
        'user'            : 'dummy_user',
        'project'         : gen_random_project(),
        'bc'              : gen_random_tb(),
        'tb'              : gen_random_tb(),
        'status'          : gen_random_status(),
        'tool_ver'        : gen_random_tool_ver(),
        'tests'           : gen_test_list(),
        'is_parent'       : False,
        'is_jenkins'      : False,
        'c_time'          : datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S'),
    }

def update_child_data():
    return {
        'status': gen_random_status(),
        'is_alive': gen_random_bool(),
        'last_alive': datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S'),
    }

def update_parent_data():
    return {
        'is_alive': gen_random_bool(),
        'last_alive': datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S'),
        'status': gen_random_status(),
        'is_multi_inst': gen_random_bool()
    }