import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from . import app_config

# Define the tables to be created in the database.
db = SQLAlchemy()

class Items_MELI(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.String(100), primary_key=True)
    price = db.Column(db.String(100))
    start_time = db.Column(db.String(100))
    name = db.Column(db.String(100))
    description = db.Column(db.String(100))
    nickname = db.Column(db.String(100))

def create_app():
    """ This function creates a flask app and pushes links it to 
        the database engine """

    flask_app = Flask(__name__)
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = app_config.DATABASE_CONNECTION_URI
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    flask_app.app_context().push()
    db.init_app(flask_app)
    db.create_all()
    return flask_app
