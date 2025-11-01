from .schemas import Customer_Schema, Customers_Schema, login_schema
from flask import request, jsonify
from app.models import db, Customer
from marshmallow import ValidationError
from . import customers_bp
from app.extensions import limiter, cache
from app.utils.util import encode_token, token_required

@customers_bp.route('/login', methods=['POST'])
def customer_login():
    try:
        credentials = login_schema.json(request.json)
        email = credentials['email']
        password = credentials['password']
    except ValidationError as e:
        return jsonify(e.message), 400
    
    query = db.select(Customer).where(Customer.email == email)
    customer = db.session.execute(query).scalars().first()

    if customer and customer.password == password:
        token = encode_token(customer.id)
        
        response = {
            "status": "success",
            "message": "Login successful",
            "token": token
        }
        return jsonify(response), 200
    else:
        return jsonify({"message": "Invalid email or password"}), 401
    
@customers_bp.route('/', methods=['POST']) 
def create_customer():
    try:
        customer_data = Customer_Schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    query = db.select(Customer).where(Customer.email == customer_data['email']) #does this email already exists?
    existing_customer = db.session.execute(query).scalars().all()
    if existing_customer:
        return jsonify({"message": "Customer with this email already exists."}), 400
    
    new_customer = Customer(**customer_data)
    db.session.add(new_customer)
    db.session.commit()
    
    return Customer_Schema.jsonify(new_customer)

@customers_bp.route('/', methods=['GET'])
@limiter.limit("10 per minute")#limits amount of requests to avoid abuse
@cache.cached(timeout=120)#caches in case of frequent reads
def get_customers():
    all_customers = db.session.execute(db.select(Customer)).scalars().all()
    return Customers_Schema.jsonify(all_customers)
@customers_bp.route('/<int:id>', methods=['GET'])
def get_customer(id):
    customer = db.session.get(Customer, id)
    if not customer:
        return jsonify({"message": "Customer not found."}), 404
    return Customer_Schema.jsonify(customer)

@customers_bp.route('/<int:id>', methods=['PUT'])
@cache.cached(timeout=60) #keeps this info close in case of frequent updates
@token_required
def update_customer(id):
    customer = db.session.get(Customer, id)
    if not customer:
        return jsonify({"message": "Customer not found."}), 404
    try:
        customer_data = Customer_Schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    for key, value in customer_data.items():
        setattr(customer, key, value)
    
    db.session.commit()
    return Customer_Schema.jsonify(customer)

    
@customers_bp.route('/', methods=['DELETE'])
@token_required
def delete_customer(user_id):
    query = db.select(Customer).where(Customer.id == user_id)
    customer = db.session.execute(query).scalars().first()
    
    db.session.delete(customer)
    db.session.commit()
    return jsonify({"message": "customer deleted successfully."})