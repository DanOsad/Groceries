import json
from uuid import uuid4
from sqlalchemy import delete
from models.customers     import Customers
from flask      import Blueprint, request
from extensions import tools, Response, db

customer_routes = Blueprint('customer_routes', __name__)

@customer_routes.route('/customer', methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def im_alive():
    resp = Response()

    tools.log_request(request)

    resp.set_msg('OK')
    resp.set_success()
    resp.set_data({'customer': True})

    return tools._respond(request, **resp.serialize())

@customer_routes.route('/create-customer', methods=['POST'])
def create_customer():
    resp = Response()

    try:
        # Log the request
        tools.log_request(request)

        # Extract data from the request
        data = request.get_json()
        name = data.get('name')

        # Validate input data
        if not name:
            resp.set_msg('Name is required')
            resp.set_failure()
            return tools._respond(request, **resp.serialize())

        # Create a new customer object
        # new_customer = Customers(id=str(uuid4()), name=name)
        new_customer = Customers(guid=uuid4(), name=name)

        # Add the new customer to the database
        db.session.add(new_customer)
        db.session.commit()

        # Set success response
        resp.set_msg('Customer created successfully')
        resp.set_success()
        resp.set_data({'customer': new_customer.as_dict})

    except Exception as e:
        db.session.rollback()
        resp.set_msg(f'Error: {str(e)}')
        resp.set_failure()

    return tools._respond(request, **resp.serialize())