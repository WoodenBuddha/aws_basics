# main/__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import config_by_name

db = SQLAlchemy()
app = None


def create_app(config_name):
    global app
    if app == None:
        app = Flask(__name__)
        app.config.from_object(config_by_name[config_name])
        app.config['SECRET_KEY'] = 'you-will-never-guess'
        db.init_app(app)

    return app