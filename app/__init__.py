from flask import Flask
from flask_jwt_extended import JWTManager
from flask_pymongo import PyMongo
from flask_mail import Mail

db = PyMongo()
jwt = JWTManager()
mail = Mail()

def create_app(config_class):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    db.init_app(app)
    jwt.init_app(app)
    mail.init_app(app)
    
    from app.routes import root_routes, auth_routes, user_routes
    app.register_blueprint(root_routes.bp)
    app.register_blueprint(auth_routes.bp)
    app.register_blueprint(user_routes.bp)
    
    return app