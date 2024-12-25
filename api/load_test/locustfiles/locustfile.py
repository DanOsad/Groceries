import sys
sys.dont_write_bytecode = True

import json, random
import dummy_data
from weights import *
from store import StoreRows
from locust import HttpUser, events, task, between



class SimbaUser(HttpUser):
    wait_time = between(3, 10)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.timeout = 5

    ### CREATE ###
    @task(weight=create_parent_children_weight)
    def build_parent_and_children(self):
        # Create parent
        parent_id = self.create_parent()

        # Create children
        if parent_id: self.create_children(parent_id)

    def create_parent(self):
        data = dummy_data.create_parent_data()
        res = self.client.post(f'/new_job2', data=data, timeout=self.timeout)
        if res.status_code == 201:
            parent_id = int(res.content)
            StoreRows.created_parents.append(parent_id)
            return parent_id
        
        return None
    
    def create_children(self, parent_id: int):
        data = dummy_data.create_children_data()#.update({'parent_id': parent_id})
        data['parent_id'] = parent_id
        res = self.client.post(f'/create_children', json=json.dumps(data), timeout=self.timeout)

        if res.json()['success']:
            StoreRows.created_children.extend( list( res.json()['rows'].values() ) )

    ### UPDATE ###
    # @task(weight=100)
    def update_parent_and_children(self):
        # Update parent
        self.update_random_parent_and_children()
        # Update children
        self.update_random_child()

    @task(weight=update_parent_weight)
    def update_random_parent_and_children(self):
        if StoreRows.created_parents:
            parent_id = random.choice(seq=StoreRows.created_parents)
            data = dummy_data.update_parent_data()
            data['parent_id'] = parent_id
            self.client.patch(f'/update_job2/{parent_id}', data=data, timeout=self.timeout, name='update_job2')

    @task(weight=update_child_weight)
    def update_random_child(self):
        if StoreRows.created_children:

            children = random.sample(StoreRows.created_children, k=random.randint(0, len(StoreRows.created_children)))

            for child_id in children:
                self.client.patch(f'/update_job2/{child_id}', data=dummy_data.update_child_data(), timeout=self.timeout, name='update_job2')

    ### GET ###
    # @task(weight=10)
    def get_parent_and_children(self):
        if StoreRows.created_parents:
            parent_id = random.choice(StoreRows.created_parents)
            # Get parent
            self.get_parent(parent_id)
            # Get children
            self.get_children(parent_id)

    @task(weight=get_parent_weight)
    def get_parent(self):
        if StoreRows.created_parents:
            parent_id = random.choice(StoreRows.created_parents)
            self.client.get(f'/get_job/{parent_id}', timeout=self.timeout, name='get_job')

    @task(weight=get_children_weight)
    def get_children(self):
        if StoreRows.created_parents:
            parent_id = random.choice(StoreRows.created_parents)
            self.client.get(f'/get_children/{parent_id}', timeout=self.timeout, name='get_children')

    #### KILL ###
    @task(weight=kill_weight)
    def kill(self):
        # Kill parent
        self.kill_random_parent_and_children()
        # Kill children
        self.kill_random_child()

    def kill_random_parent_and_children(self):
        if StoreRows.created_parents:
            parent_id = random.choice(seq=StoreRows.created_parents)
            self.client.put(f'/kill_parent/{parent_id}', timeout=self.timeout, name='kill_parent')

    def kill_random_child(self):
        if StoreRows.created_children:
            child_id = random.choice(seq=StoreRows.created_children)
            self.client.put(f'/killed/{child_id}', timeout=self.timeout, name='killed')

    def cleanup(self):
        if StoreRows.created_parents or StoreRows.created_children:
            del_list = StoreRows.created_parents + StoreRows.created_children
            data = {"del_list": del_list}
            self.client.delete('/delete', json=json.dumps(data), timeout=self.timeout)

@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    if StoreRows.created_parents or StoreRows.created_children:
        SimbaUser(environment).cleanup()