import flask
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from decouple import config
import os
from csflask.config import Config


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
mail = Mail()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from csflask.users.routes import users
    from csflask.details.routes import details
    from csflask.main.routes import main
    from csflask.errors.error_handler import errors

    app.register_blueprint(users)
    app.register_blueprint(details)
    app.register_blueprint(main)
    app.register_blueprint(errors)
    
    return app

# $ python
# >>> from flask_blog import create_app
# >>> app = create_app()
# >>> app.app_context().push()
# >>> from flask_blog import db
# >>> db.create_all()

