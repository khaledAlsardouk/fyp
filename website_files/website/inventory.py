from os import path
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, current_user
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, flash, redirect, Blueprint
import datetime
from .models import Inventory

DB_NAME = "Inventory.db"
Inventory1 = Blueprint("Inventory", __name__)
data = []

choice = 0

heading = ("Item name", "Expiry", "notfication date", "Category")


@Inventory1.route('/inventory', methods=['GET', 'POST'])
def inventory():
    global choice
    if choice == 0:
        items = Inventory.query.all()
        for item in items:
            data.append([item.Item_name, item.Expiry.date(), item.notfication_date.date(), item.Category])
        choice = 1
    return render_template("helloworld.html", headings=heading, datas=data)
