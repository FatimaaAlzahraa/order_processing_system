from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os

from .error_handlers import register_error_handlers

db = SQLAlchemy()
mail = Mail()
jwt = JWTManager()

load_dotenv()  # load env variables

def create_app():
    app = Flask(__name__)
    app.config.from_object("config")
    jwt = JWTManager(app)
    #load JWT key from .env
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

    db.init_app(app)
    mail.init_app(app)
    register_error_handlers(app)
    jwt.init_app(app)

    from .routes import main
    app.register_blueprint(main)

    return app

