from os import path
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, flash, redirect
from flask_login import mixins
import datetime
import requests
from datetime import date
app = Flask(__name__)

app.secret_key = "blue red green k"

db = SQLAlchemy(app)
DB_NAME = "test.db"
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'


class Inventory(db.Model):
    __tablename__ = "inventory"             #to be user name using cookie or login manager
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
        data.append([item.Item_name,(item.Expiry).date(),(item.notfication_date).date(),item.Category])

def Get_Time(expiry,current_date):
    expiry = datetime.strptime(expiry, "%Y-%m-%d")
    current_date = datetime.strptime(current_date, "%Y-%m-%d")
    if expiry - current_date > 7:
        return False
    else: return True

def Get_Recipe_From_Date():
    url = "https://edamam-recipe-search.p.rapidapi.com/search"
    ingredients = ''
    items = Inventory.query.all()
    for item in items:
        if item.Category == "Food" and (Get_Time(item.Expiry,date.today) == True):
            ingredients = ingredients + item.Item_name + ", "
            print(ingredients)
    querystring = {"q": ingredients}

    headers = {
        "X-RapidAPI-Host": "edamam-recipe-search.p.rapidapi.com",
        "X-RapidAPI-Key": "c82513b996msh91aa04854473575p15db2ajsn8d757b1e5a57"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    print(response.text)

def Get_Recipe_From_User():
    url = "https://edamam-recipe-search.p.rapidapi.com/search"
    ingredients = input("Please enter your desired ingredient(s)")
    querystring = {"q": ingredients}

    headers = {
        "X-RapidAPI-Host": "edamam-recipe-search.p.rapidapi.com",
        "X-RapidAPI-Key": "c82513b996msh91aa04854473575p15db2ajsn8d757b1e5a57"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    print(response.text)

@app.route('/', methods=['GET', 'POST'])
def index():
    create_database(app)
    GetALLItem()
    Get_Recipe_From_Date()
    Get_Recipe_From_User()
    return render_template("helloworld.html",headings=heading,datas=data)





if __name__ == "__main__":
    app.run(debug=True)
