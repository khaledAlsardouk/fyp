from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class User(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    First_name=db.Column(db.String(255),nullable=False)
    Last_name=db.Column(db.String(255),nullable=False)
    Email=db.Column(db.String(255),nullable=False, unique=False)
    Password=db.Column(db.String(255),nullable=False)

class Item(db.Model):
    __tablename__ = "Items"
    id = db.Column(db.Integer, primary_key=True)
    Barcode = db.Column(db.String(255), nullable=False)
    Item_name = db.Column(db.String(255), nullable=False)
    Category = db.Column(db.String(255), nullable=False)

class Inventory(db.Model,UserMixin):
    __tablename__ = "inventory"
    id = db.Column(db.Integer, primary_key=True)
    Item_name = db.Column(db.String(255), nullable=False)
    Expiry = db.Column(db.DateTime, nullable=False)
    notfication_date = db.Column(db.DateTime, nullable=False, unique=False)
    Category = db.Column(db.String(255), nullable=False)