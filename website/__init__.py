from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
import os
from flask_login import LoginManager


db = SQLAlchemy()
DB_NAME = "database.db"
db_path = os.path.join(os.path.dirname(__file__), DB_NAME)   


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'alx24'  
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'  
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Message, Cart

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
        
    return app

def create_database(app):   
    if not path.exists(db_path):
            with app.app_context():
                db.create_all()
                print('Created Database!')
