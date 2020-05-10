import json

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

from flaskr import config
from flaskr.logic.app_logic import main

# Create flask app
app = Flask(__name__)

# URI to connect to the Postgres database, imported from config.py
app.config['SQLALCHEMY_DATABASE_URI'] = config.DATABASE_CONNECTION_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Items_MELI(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.String(100), primary_key=True)
    price = db.Column(db.String(100))
    start_time = db.Column(db.String(100))
    name = db.Column(db.String(100))
    description = db.Column(db.String(100))
    nickname = db.Column(db.String(100))

# Create table defined above
db.create_all()

@app.route('/', methods=['GET'])
def fetch():
    items = Items_MELI.query.all()
    all_items = []
    for item in items:
        new_item = {
                "id": item.id,
                "price": item.price,
                "start_time": item.start_time,
                "name": item.name,
                "description": item.description,
                "nickname": item.nickname
        }

        all_items.append(new_item)
    return json.dumps(all_items), 200

@app.route('/delete_all', methods=['GET'])
def remove_all():
    print(db.MetaData())
    db.drop_all()
    db.create_all()
    return "Table deleted"

        
@app.route('/upload_file', methods=['GET'])
def upload_all():
    return main()
