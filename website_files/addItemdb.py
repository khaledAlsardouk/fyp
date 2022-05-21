from os import path

from sqlalchemy import null
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, current_user

from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template
import datetime


def create_database(app):
    if not path.exists('/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')


app = Flask(__name__)

app.secret_key = "blue red green k"
DB_NAME = "Users.db"
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    First_name = db.Column(db.String(255), nullable=False)
    Last_name = db.Column(db.String(255), nullable=False)
    Email = db.Column(db.String(255), nullable=False, unique=False)
    Password = db.Column(db.String(255), nullable=False)
    Inventory = db.relationship('Inventory')


class Item(db.Model):
    __tablename__ = "Items"
    id = db.Column(db.Integer, primary_key=True)
    Barcode = db.Column(db.String(255), nullable=False)
    Item_name = db.Column(db.String(255), nullable=False)
    Category = db.Column(db.String(255), nullable=False)


class Inventory(db.Model):
    __tablename__ = "inventory"
    id = db.Column(db.Integer, primary_key=True)
    Item_name = db.Column(db.String(255), nullable=False)
    Expiry = db.Column(db.String(255), nullable=False)
    Category = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


@app.route('/', methods=['GET', 'POST'])
def index():
    create_database(app)
    item1 = Inventory(Item_name="flour",Expiry=str(datetime.date(2022, 5, 25)),Category="food",user_id=1)
    db.session.add(item1)
    db.session.commit()
    item1 = Inventory( Item_name="hummus", Expiry=str(datetime.date(2022, 5, 26)),
                      Category="food", user_id=1)
    db.session.add(item1)
    db.session.commit()
    item1 = Inventory(Item_name="chocolate", Expiry=str(datetime.date(2022, 5, 27)),
                      Category="food", user_id=1)
    db.session.add(item1)
    db.session.commit()
    item1 = Inventory(Item_name="sugar", Expiry=str(datetime.date(2026, 5, 27)),
                      Category="food", user_id=1)
    db.session.add(item1)
    db.session.commit()

    item1 = Inventory(Item_name="popcorn", Expiry=str(datetime.date(2026, 5, 27)),
                      Category="food", user_id=1)
    db.session.add(item1)
    db.session.commit()

    return render_template("helloworld.html")


if __name__ == '__main__':
    app.run(debug=True)
