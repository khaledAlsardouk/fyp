from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('passwords')

        user = User.query.filter_by(Email=email).first()
        if user:
            if check_password_hash(user.Password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)

                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


Specialchar = ['$', '@', '#', '%', '_']


@auth.route('/Sign-Up', methods=['GET', 'POST'])
def Sign_up():
    if request.method == 'POST':
        FirstName = request.form.get('First_Name')
        LastName = request.form.get('Last_Name')
        email = request.form.get('email')
        Password = request.form.get('password')
        user = User.query.filter_by(Email=email).first()
        if user == User():
            flash('Email already exists.', category='error')
        elif len(Password) < 5:
            flash('the password must be more than 8 characters', category="error")
        elif not any(char.isdigit() for char in Password):
            flash('the password must contain at least one digit', category="error")
        elif not any(char.isupper() for char in Password):
            flash('the password must contain at least one capital letter', category="error")
        elif not any(char in Specialchar for char in Password):
            flash('the password must contain at least one special character such as $,_,@,#,%', category="error")
        else:
            new_user = User(First_name=FirstName, Last_name=LastName, Email=email,
                            Password=generate_password_hash(Password, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash('Account created!', category='success')
            login_user(new_user, remember=True)

            return redirect(url_for('views.home'))
    return render_template("Sign-Up.html", user=current_user)
