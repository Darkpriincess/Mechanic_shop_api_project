
class DevelopmentConfig:    
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:Dessa.24@localhost/mechanic_shop_db'
    DEBUG = True

class TestingConfig:
    pass

class ProductionConfig:
    pass