import os
from flask import Flask
import flask_sqlalchemy
import flask_sqlalchemy

from .logic.models import db
from . import config


def create_app():
    flask_app = Flask(__name__)

    # URI to connect to the Postgres database, imported from config.py
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = config.DATABASE_CONNECTION_URI
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    print(flask_app.config)

    # Specify to SQLAlchemy which app is to be used.
    flask_app.app_context().push()

    # Link database to Flask app.
    db.init_app(flask_app)

    # Create all tables (specified in models.py) if non existant.
    db.create_all()

    return flask_app
# Define the tables to be created in the database.

db = flask_sqlalchemy.SQLAlchemy(flask_app)


class Items_MELI(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.String(100), primary_key=True)
    price = db.Column(db.Integer)
    start_time = db.Column(db.String(100))
    name = db.Column(db.String(100))
    description = db.Column(db.String(100))
    nickname = db.Column(db.String(100))


