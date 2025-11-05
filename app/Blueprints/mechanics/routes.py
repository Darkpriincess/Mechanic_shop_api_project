from flask import request, jsonify
from app.models import db, Mechanic
from . import mechanics_bp
from .schemas import Mechanic_Schema, Mechanics_Schema, login_schema
from marshmallow import ValidationError
from app.extensions import limiter, cache
from app.utils.util import encode_token, token_required

@mechanics_bp.route('/login', methods=['POST'])
def mechanic_login():
    try:
        credentials = login_schema.json(request.json)
        email = credentials['email']
        password = credentials['password']
    except ValidationError as e:
        return jsonify(e.message), 400
    
    query = db.select(Mechanic).where(Mechanic.email == email)
    mechanic = db.session.execute(query).scalars().first()

    if mechanic and mechanic.password == password:
        token = encode_token(mechanic.id)
        
        response = {
            "status": "success",
            "message": "Login successful",
            "token": token
        }
        return jsonify(response), 200
    else:
        return jsonify({"message": "Invalid email or password"}), 401

@mechanics_bp.route('/', methods=['POST'])
def create_mechanic():
    try:
        mechanic_data = Mechanic_Schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    query = db.select(Mechanic).where(Mechanic.email == mechanic_data['email']) #does this email already exists?
    existing_mechanic = db.session.execute(query).scalars().all()
    if existing_mechanic:
        return jsonify({"message": "Mechanic with this email already exists."}), 400
    
    new_mechanic = Mechanic(**mechanic_data)
    db.session.add(new_mechanic)
    db.session.commit()
    
    return Mechanic_Schema.jsonify(new_mechanic)

@mechanics_bp.route('/', methods=['GET'])
@limiter.limit("10 per minute")#limits amount of requests to avoid abuse
@cache.cached(timeout=120)#caches in case of frequent reads
def get_mechanics():
    all_mechanics = db.session.execute(db.select(Mechanic)).scalars().all()
    return Mechanics_Schema.jsonify(all_mechanics)

@mechanics_bp.route('/<int:id>', methods=['GET'])
def get_mechanic(id):
    mechanic = db.session.get(Mechanic, id)
    if not mechanic:
        return jsonify({"message": "Mechanic not found."}), 404
    return Mechanic_Schema.jsonify(mechanic)

@mechanics_bp.route('/<int:id>', methods=['PUT'])
@cache.cached(timeout=60) #keeps this info close in case of frequent updates
@token_required
def update_mechanic(id):
    mechanic = db.session.get(Mechanic, id)
    if not mechanic:
        return jsonify({"message": "Mechanic not found."}), 404
    try:
        mechanic_data = Mechanic_Schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    for key, value in mechanic_data.items():
        setattr(mechanic, key, value)
    
    db.session.commit()
    return Mechanic_Schema.jsonify(mechanic)

@mechanics_bp.route('/<int:id>', methods=['DELETE'])
@token_required
def delete_mechanic(id):
    mechanic = db.session.get(Mechanic, id)
    if not mechanic:
        return jsonify({"message": "Mechanic not found."}), 404
    db.session.delete(mechanic)
    db.session.commit() 
    return jsonify({"message": "Mechanic deleted successfully."})

