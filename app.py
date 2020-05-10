from flask import jsonify
from sqlalchemy.exc import IntegrityError

from templates.page import home_page
from logic.models import db, create_app, Items_MELI
from logic.app_logic import main

# Create flask app
app = create_app()

@app.route('/', methods=['GET'])
def page():
    return home_page

@app.route('/print_table', methods=['GET'])
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
    return jsonify(all_items)

@app.route('/delete_all', methods=['GET'])
def remove_all():
    db.drop_all()
    db.create_all()
    return "Table deleted"

        
@app.route('/gather_and_upload', methods=['GET'])
def upload_all():
    try:
        return main()
    except IntegrityError:
        return """Attempting to upload duplicate
            keys, reset table and try again."""
