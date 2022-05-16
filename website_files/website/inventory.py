from os import path
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, current_user, login_required, user_logged_in
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, flash, redirect, Blueprint
import datetime
from .models import Inventory


Inventory1 = Blueprint("Inventory", __name__)

choice = 0

<<<<<<< Updated upstream
heading = ("Item name", "Expiry", "notfication date", "Category")
data = []


def GetALLItem():
    items = Inventory.query.all()
    for item in items:
        data.append([str(item.id), item.Item_name, (item.Expiry).date(), (item.notfication_date).date(), item.Category])
=======
heading = ("Item name", "Expiry", "notfication date", "Category","User_id","usrename")
>>>>>>> Stashed changes


@Inventory1.route('/inventory', methods=['GET', 'POST'])
@login_required
def inventory():
    global choice,data
    data = []
    if choice == 0:
<<<<<<< Updated upstream
        GetALLItem()
        choice = 1
    if request.method == 'POST':
        data = []
        print(request.form['clicked_btn'])
        delete = Inventory.query.filter_by(id=request.form['clicked_btn']).first()
        Inventory.session.delete(delete)
        Inventory.session.commit()
        GetALLItem()
        return render_template("Inventory.html", headings=heading, datas=data)
    return render_template("Inventory.html", headings=heading, datas=data)
=======
        items = Inventory.query.filter_by(user_id=current_user.id)
        for item in items:         
            data.append([item.Item_name,item.Expiry, item.notfication_date, item.Category,item.user_id,current_user.First_name])
        choice = 1
    return render_template("helloworld.html", headings=heading, datas=data,user=current_user)
>>>>>>> Stashed changes
