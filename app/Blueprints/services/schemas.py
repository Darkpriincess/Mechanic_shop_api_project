from app.extensions import ma
from app.models import Service

class ServiceSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Service
        include_fk = True
        
Service_Schema = ServiceSchema()
Services_Schema = ServiceSchema(many=True)