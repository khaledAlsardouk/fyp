from os import path
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, current_user
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, flash, redirect
import datetime

app = Flask(__name__)

app.secret_key = "blue red green k"

db = SQLAlchemy(app)
DB_NAME = "test.db"
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'


class Inventory(db.Model,UserMixin):
    __tablename__ = current_user             #to be user name using cookie or login manager
    id = db.Column(db.Integer, primary_key=True)
    Item_name = db.Column(db.String(255), nullable=False)
    Expiry = db.Column(db.DateTime, nullable=False)
    notfication_date = db.Column(db.DateTime, nullable=False, unique=False)
    Category = db.Column(db.String(255), nullable=False)



heading = ("Item name","Expiry","notfication date","Category")
data=[]

def create_database(app):
    if not path.exists('/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')

@app.before_first_request
def GetALLItem():
    items = Inventory.query.all()
    for item in items:
        data.append([item.Item_name, item.Expiry.date(), item.notfication_date.date(), item.Category])
    

@app.route('/', methods=['GET', 'POST'])
def index():
    create_database(app)
    return render_template("helloworld.html",headings=heading,datas=data)





if __name__ == "__main__":
    app.run(debug=True)
