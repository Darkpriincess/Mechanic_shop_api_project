from app.extensions import ma
from app.models import Customer

class CustomerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Customer
        
Customer_Schema = CustomerSchema()
Customers_Schema = CustomerSchema(many=True)
login_schema = CustomerSchema(only=("email", "password"))