from unicodedata import category
from flask import Flask, render_template, Response, request, flash, Blueprint
import cv2
import datetime, time
from flask_login import current_user, login_required
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import null
from . import db
from .models import Item, Inventory
from flask import Flask, render_template, request, flash, redirect
import datetime
import requests
from datetime import date
import urllib
from random import randint

recipe = Blueprint("recipe", __name__)

IDS = {-1}
APP_ID = "6320241"
API_KEY = "c82513b996msh91aa04854473575p15db2ajsn8d757b1e5a57"
URL = f'https://api.edamam.com/search?/app_id=${APP_ID}&app_key=${API_KEY}'

heading = "Item name"
data = []
recipe_pic = [[] for i in range(5)]
recipe_array = [[] for i in range(5)]
recipe_label = [[] for i in range(5)]
ingredient_line = [[] for i in range(5)]
recipe_url = [[] for i in range(5)]
index = 0
select = 0
recipe_data = []



def GetALLItem():
    items = Inventory.query.filter_by(user_id=current_user.id).all()
    for item in items:
        data.append([item.Item_name])


def Get_Recipe_From_User():
    x = randint(0,20)
    success = False
    global index
    index = 0
    global recipe_data
    while not success:
        ingredients = Get_Ingredient()
        recipe_data = make_request(get_url_q(ingredients,_from = x , to=x+5))
        recipe_data = recipe_data['hits']
        if len(recipe_data) > 0:
            success = True
    index = display_recipe_labels(recipe_data, index)


def select_recipe(data, max_index):
    select = Get_Index()
    invalid = True
    while invalid:
        if select is None:
            select = 1
        if select == -1:
            select = select_recipe_from_index(max_index)
        if select == 'm':
            display_recipe_labels(data, 0)
            select = select_recipe_from_index(max_index)
        if select == 'q':
            print()
            return
        try:
            select = int(select)
            invalid = False
        except ValueError:
            invalid = True
            select = -1

    recipe_response = data[select - 1]
    recipe = recipe_response["recipe"]
    curr_recipe = filter_response(recipe)

    display_recipe_dict(curr_recipe)


def save_recipe(curr_recipe):
    """
    Saves recipe info in database of saved recipes.
    """
    id = -1
    if id in IDS:
        id = randint(100, 999)
        # Saves ID, URI, and label to database
    C.execute("INSERT into recipes (id, uri, label) values (?, ?, ?)", (id, curr_recipe["uri"], curr_recipe["label"]))
    # Displays label to confirm correct entry
    C.execute("SELECT label FROM recipes WHERE label = ?", (curr_recipe["label"],))
    result = C.fetchall()
    print(f"    You are saving: '{result[0][0]}'")
    if input("Confirm (y/n): ").lower() == "y":
        con.commit()
    print("SAVED")
    input()
    print()


def display_recipe_labels(data, index):
    reset = [[] for i in range(5)]
    reset2 = [[] for i in range(5)]
    reset3 = [[] for i in range(5)]
    reset4 = [[] for i in range(5)]
    global recipe_array
    global recipe_url
    global ingredient_line
    global recipe_pic
    recipe_pic = reset
    recipe_url = reset2
    recipe_array = reset3
    ingredient_line = reset4
    for recipe in data:
        i = recipe['recipe']['label']
        recipe_array[index].append(i)
        index += 1
    for i in range(index):
        recipe_response = data[i]
        recipes = recipe_response["recipe"]
        curr_recipe = filter_response(recipes)

        for line in curr_recipe["ingredients_line"]:
            ingredient_line[i].append(f"{line}")
        recipe_url[i].append(f"{curr_recipe['url']}")
        recipe_pic[i].append(f"{curr_recipe['image']}")

    return index


def select_recipe_from_index(max_index):
    print(f"   Select Recipe # (1-{max_index})")
    return select_from_index(max_index)


def select_from_index(max_index):
    select = -1
    while select <= 0 or select > max_index:
        select = input("\t>> ")
        if select.lower() == 'q':
            return 'q'
        elif select.lower() == 'm':
            return 'm'
        try:
            select = int(select)
        except ValueError as e:
            print("Input must be an integer!")
            select = -1
    return select - 1


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


@recipe.route('/recipe/Recipes', methods=['POST', 'GET'])
def Get_Ingredient():
    if request.method == 'POST':
        ingredient = request.form['Ingredients']
        return ingredient


@recipe.route('/recipe/Recipes', methods=['POST', 'GET'])
def Get_Index():
    if request.method == 'POST':
        select = request.form['select']
        return select


@recipe.route('/recipe', methods=['GET', 'POST'])
def index():
    global data
    data=[]
    GetALLItem()
    if request.method == 'POST':
        Get_Recipe_From_User()
        return render_template("Recipes.html", headings=heading, datas=data, label=recipe_array,
                               ing_line=ingredient_line, recipe_url=recipe_url, recipe_pic=recipe_pic)
    return render_template("Recipes.html", headings=heading, datas=data, label=recipe_array, ing_line=ingredient_line,
                           recipe_url=recipe_url, recipe_pic=recipe_pic)
