from os import path
from requests import delete
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, current_user, login_required, user_logged_in
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, flash, redirect, Blueprint
import datetime
from .models import Inventory
from . import db
Inventory1 = Blueprint("Inventory", __name__)

choice = 0

heading = ("Item name", "Expiry", "notification date", "Category", "USERID")
data = []


def GetALLItem():
    items = Inventory.query.filter_by(user_id=current_user.id)
    for item in items:
        data.append([str(item.id), item.Item_name, item.Expiry,  item.Category, current_user.id])



@Inventory1.route('/inventory', methods=['GET', 'POST'])
@login_required
def inventory():
    global choice, data
    data = []
    GetALLItem()

    if request.method == 'POST':
        data = []
        print(request.form['clicked_btn'])
        delete=request.form['clicked_btn']
        Inventory.query.filter_by(id=delete).delete()
        db.session.commit()
        GetALLItem()
        return render_template("Inventory.html", headings=heading, datas=data)

    return render_template("Inventory.html", headings=heading, datas=data)
