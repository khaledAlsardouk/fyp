from unicodedata import category
from flask import Flask, render_template, Response, request, flash, Blueprint
import cv2
import datetime, time
from flask_login import current_user, login_required
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import null
from . import db
from .models import Item, Inventory,User,current_user
from flask import Flask, render_template, request, flash, redirect
import datetime
import requests
from datetime import datetime
from datetime import timedelta
global count
from random import randint
from dateutil import parser

Home = Blueprint("Home", __name__)

IDS = {-1}
APP_ID = "6320241"
API_KEY = "c82513b996msh91aa04854473575p15db2ajsn8d757b1e5a57"
URL = f'https://api.edamam.com/search?/app_id=${APP_ID}&app_key=${API_KEY}'

heading = ("Expiring Soon" , "Date")
data = []
recipe_pic = [[] for i in range(5)]
recipe_array = [[] for i in range(5)]
recipe_label = [[] for i in range(5)]
ingredient_line = [[] for i in range(5)]
recipe_url = [[] for i in range(5)]
index = 0
select = 0
recipe_data = []
count=0

def Get_Time(expiry, current_date):
    try:
        expiry = parser.parse(str(expiry))
        current_date = parser.parse(str(current_date))
    except Exception as inst:
        print(type(inst))    # the exception instance
        print(inst.args)     # arguments stored in .args
        print(inst)
        expiry = datetime.strptime(str(expiry), "%Y-%m-%d %H:%M:%S")
        current_date = datetime.strptime(str(current_date), "%Y-%m-%d %H:%M:%S.f")
    if expiry > current_date:
        return False
    else:
        return True



def Get_Recipe_From_User():

    global index
    index = 0
    x = randint(0,20)
    global recipe_data
    ingredients = []
    items = Inventory.query.filter_by(user_id=current_user.id).all()
    this_day = datetime.now() + timedelta(days=7)
    if items is not None:
      for item in items:
           if item.Category == "food" and (Get_Time(item.Expiry, this_day) == True):
                ingredients.append(item.Item_name)
                data.append([item.Item_name,item.Expiry])
    recipes = []
    for ing in ingredients:
         recipe_data = make_request(get_url_q(ing,_from=x, to=x+1))
         recipes.append(recipe_data['hits'])


    index = display_recipe_labels(recipes, index, len(recipes))







def display_recipe_labels(data, index, count):
    reset = [[] for i in range(count)]
    reset2 = [[] for i in range(count)]
    reset3 = [[] for i in range(count)]
    reset4 = [[] for i in range(count)]
    global recipe_array
    global recipe_url
    global ingredient_line
    global recipe_pic
    recipe_pic = reset
    recipe_url = reset2
    recipe_array = reset3
    ingredient_line = reset4
    for recipe in data:
        for re in recipe:
            i = re['recipe']['label']
            recipe_array[index].append(i)
            index += 1
    for i in range(index):
        recipe_response = data[i][0]
        recipes = recipe_response["recipe"]
        curr_recipe = filter_response(recipes)

        for line in curr_recipe["ingredients_line"]:
            ingredient_line[i].append(f"{line}")
        recipe_url[i].append(f"{curr_recipe['url']}")
        recipe_pic[i].append(f"{curr_recipe['image']}")

    return index


def display_recipe_dict(curr_recipe):
    """
    Displays dictionary curr_recipe.
    Dictionary curr_recipe keys include:
        - "ingredients_line"
        - "ingredients"
        - "label"
        - "url"
    """

    global ing_line_count
    ing_line_count = 0
    recipe_label.clear()
    ingredient_line.clear()
    recipe_url.clear()
    recipe_label.append(f"{curr_recipe['label']}")
    for line in curr_recipe["ingredients_line"]:
        ingredient_line.append(f"{line}")
        ing_line_count = ing_line_count + 1
    recipe_url.append(f"{curr_recipe['url']}")


def filter_response(recipe):
    """
    Takes response object and returns dictionary with readable
    recipe data
    """
    curr_recipe = {
        "ingredients_line": recipe["ingredientLines"],
        "ingredients": recipe["ingredients"],
        "label": recipe["label"],
        "url": recipe["url"],
        "uri": recipe["uri"],
        "image": recipe["image"]}
    return curr_recipe


def make_request(url):
    response = requests.get(url)
    data = response.json()
    return data


def get_url_q(key_word, _from=0, to=20):
    url = URL + f'&q=${key_word}&to={to}&from={_from}'
    return url


def get_url_r(uri):
    return URL + f'&r={uri}'


@Home.route('/', methods=['GET', 'POST'])
@login_required
def index():
    global data,recipe_data,recipe_pic,recipe_array,recipe_label,ingredient_line,recipe_url,index,select
    try:
        data = []
        recipe_pic = [[] for i in range(5)]
        recipe_array = [[] for i in range(5)]
        recipe_label = [[] for i in range(5)]
        ingredient_line = [[] for i in range(5)]
        recipe_url = [[] for i in range(5)]
        index = 0
        select = 0
        recipe_data = []
        Get_Recipe_From_User()
        user = User.query.filter_by(id=current_user.id).first()
        Message = "Welcome! " + user.First_name + " " + user.Last_name
        return render_template("test.html", headings=heading, datas=data, label=recipe_array, ing_line=ingredient_line,
                           recipe_url=recipe_url, recipe_pic=recipe_pic,recipe_count=index,Welcome= Message,index=index)
    except:
        return render_template("test.html", headings=heading, datas=[], label=[], ing_line=[],
                               recipe_url=[], recipe_pic=[], recipe_count=0, Welcome="Message",index=0)

