from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
class User(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    First_name=db.Column(db.String(255),nullable=False)
    Last_name=db.Column(db.String(255),nullable=False)
    Email=db.Column(db.String(255),nullable=False, unique=False)
    Password=db.Column(db.String(255),nullable=False)