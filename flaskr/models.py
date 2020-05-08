# Define the tables to be created in the database.
import flask_sqlalchemy

db = flask_sqlalchemy.SQLAlchemy()


class Items_MELI(db.Model):
    __tablename__ = 'items'
    site = db.Column(db.String(100))
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer)
    start_time = db.Column(db.String(100))
    name = db.Column(db.String(100))
    description = db.Column(db.String(100))
    nickname = db.Column(db.String(100))

