import json

from flask import request

from . import create_app
from .models import Items_MELI, db

app = create_app()


@app.route('/', methods=['GET'])
def fetch():
    items = Items_MELI.query.all()
    all_items = []
    for item in items:
        new_item = {
                "site": item.site,
                "id": item.id,
                "price": item.price,
                "start_time": item.start_time,
                "name": item.name,
                "description": item.description,
                "nickname": item.nickname
        }

        all_items.append(new_item)
    return json.dumps(all_items), 200

@app.route('/add', methods=['GET'])
def add():
    return request.args 
#    data = request.get_json()
#    site = data['site']
#    id = data['id']
#    price = data['price']
#    start_time = data['start_time']
#    name = data['name']
#    description = data['description']
#    nickname = data['nickname']

#    item = Items_MELI(site=site, id=id, price=price, start_time=start_time, name=name, description=description, nickname=nickname)
#    db.session.add(item)
#    db.session.commit()
#    return json.dumps("Added"), 200
        
@app.route('/upload_file', methods=['GET'])
def upload_all():
    main()
