from flask import Flask
from .extensions import ma, limiter, cache
from .models import db
from .Blueprints.customers import customers_bp
from .Blueprints.mechanics import mechanics_bp
from .Blueprints.services import services_bp

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(f'config.{config_name}')
    
    #initialize extensions
    ma.init_app(app)
    db.init_app(app)
    limiter.init_app(app)
    cache.init_app(app)
    
    #Register Blueprints
    app.register_blueprint(customers_bp, url_prefix='/customers')
    app.register_blueprint(mechanics_bp, url_prefix='/mechanics')
    app.register_blueprint(services_bp, url_prefix='/services')
    
    return app