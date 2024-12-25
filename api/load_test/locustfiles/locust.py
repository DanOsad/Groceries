import sys
sys.dont_write_bytecode = True

import json, random
from locust import HttpUser, task, between
import dummy_data

# Store created rows
created_parents = []
created_children = []

class CreateSimbaObjs(HttpUser):
    wait_time = between(5, 10)

    @task(2)
    def build_parent_and_children(self):
        # Create parent
        self.parent_id = self.create_parent()

        # Create children
        if self.parent_id: self.create_children(self.parent_id)

    def create_parent(self):
        data = dummy_data.create_parent_data()
        res = self.client.post(f'/new_job2', data=data, timeout=15)
        if res.status_code == 201:
            parent_id = int(res.content)
            created_parents.append(parent_id)
            return parent_id
        
        return None

    def create_children(self, parent_id: int):
        data = dummy_data.create_children_data()#.update({'parent_id': parent_id})
        data['parent_id'] = parent_id
        res = self.client.post(f'/create_children', json=json.dumps(data), timeout=15)

        if res.json()['success']:
            created_children.extend( list( res.json()['rows'].values() ) )

class GetSimbaObjs(HttpUser):
    wait_time = between(1, 5)

    @task(4)
    def get_parent_and_children(self):
        # Get parent
        parent_id = random.choice(dummy_data.sample_parent_ids)
        self.get_parent(parent_id)
        # Get children
        self.get_children(parent_id)

    def get_parent(self, parent_id):
        self.client.get(f'/get_job/{parent_id}')

    def get_children(self, parent_id):
        self.client.get(f'/get_children/{parent_id}')

class UpdateSimbaObjs(HttpUser):
    wait_time = between(1, 5)

    @task(4)
    def update_parent_and_children(self):
        # Update parent
        self.update_random_parent_and_children()
        # Update children
        self.update_random_child()

    def update_random_parent_and_children(self):
        if created_parents:
            parent_id = random.choice(seq=created_parents)
            data = dummy_data.update_parent_data()
            data['parent_id'] = parent_id
            self.client.post(f'/update_parent', data=data, timeout=15)

    def update_random_child(self):
        if created_children:
            child_id = random.choice(seq=created_children)
            self.client.patch(f'/update_job2/{child_id}', data=dummy_data.update_child_data(), timeout=15)

class KillSimbaObjs(HttpUser):
    wait_time = between(1, 5)

    @task(1)
    def kill(self):
        # Kill parent
        self.kill_random_parent_and_children()
        # Kill children
        self.kill_random_child()

    def kill_random_parent_and_children(self):
        if created_parents:
            parent_id = random.choice(seq=created_parents)
            self.client.put(f'/kill_parent/{parent_id}')

    def kill_random_child(self):
        if created_children:
            child_id = random.choice(seq=created_children)
            self.client.put(f'/killed/{child_id}')


#TODO: Create Simba/User class that simulated simba process then run many workers
"""
class TestUser(HttpUser):
    wait_time = between(0.5, 2.5)
    tasks = [fast_task, slow_task, ProcessNumberTask]
    login_token = ''
    is_login = False

    def on_start(self):
        with self.client.post('/login', json={'username': 'username', 'password': 'password'}) as response:
            if response.status_code == 200:
                self.login_token = response.json()['token']
                self.is_login = True

    def on_stop(self):
        with self.client.get('/logout') as response:
            if response.status_code == 200:
                self.login_token = ''
                self.is_login = False
"""