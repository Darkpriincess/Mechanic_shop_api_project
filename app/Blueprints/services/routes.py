from flask import request, jsonify
from app.models import db, Service  
from marshmallow import ValidationError
from .schemas import Service_Schema, Services_Schema
from . import services_bp
from app.models import Customer
from app.extensions import limiter, cache



@services_bp.route('/', methods=['POST'])
def create_service():
    try:
        service_data = Service_Schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    new_service = Service(**service_data)
    db.session.add(new_service)
    db.session.commit()
    return Service_Schema.jsonify(new_service)



@services_bp.route('/<ticket_id>/assign_mechanic/<mechanic_id>', methods=['PUT'])
def assign_mechanic_to_service(ticket_id, mechanic_id):
    service = db.session.get(Service, ticket_id)
    if not service:
        return jsonify({"message": "Service not found."}), 404
    
    service.mechanic_id = mechanic_id
    db.session.commit()
    
    return Service_Schema.jsonify(service)

@services_bp.route('/<ticket_id>/remove_mechanic/<mechanic_id>', methods=['PUT'])
def remove_mechanic_from_service(ticket_id, mechanic_id):
    service = db.session.get(Service, ticket_id)
    if not service:
        return jsonify({"message": "Service not found."}), 404
    
    if service.mechanic_id != mechanic_id:
        return jsonify({"message": "This mechanic is not assigned to the service."}), 400
    
    service.mechanic_id = None
    db.session.commit()
    
    return Service_Schema.jsonify(service)

@services_bp.route('/', methods=['GET'])
def get_services():
    all_services = db.session.execute(db.select(Service)).scalars().all()
    return Services_Schema.jsonify(all_services)

