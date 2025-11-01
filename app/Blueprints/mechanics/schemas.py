from app.extensions import ma
from app.models import Mechanic

class MechanicSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Mechanic
        
Mechanic_Schema = MechanicSchema()
Mechanics_Schema = MechanicSchema(many=True)
login_schema = MechanicSchema(only=("email", "password"))