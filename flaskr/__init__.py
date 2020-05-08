import os
from flask import Flask
import flask_sqlalchemy

from .models import db
from . import config


def create_app():
    flask_app = Flask(__name__)

    # URI to connect to the Postgres database, imported from config.py
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = config.DATABASE_CONNECTION_URI
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Add environment variables to connect to database.
    os.environ['POSTGRES_USER'] = 'test'
    os.environ['POSTGRES_PASSWORD'] = 'password'
    os.environ['POSTGRES_HOST'] = 'localhost'
    os.environ['POSTGRES_PORT'] = '5432'
    os.environ['POSTGRES_DB'] = 'example'

    # Specify to SQLAlchemy which app is to be used.
    flask_app.app_context().push()

    # Link database to Flask app.
    db.init_app(flask_app)

    # Create all tables (specified in models.py) if non existant.
    db.create_all()

    return flask_app

