
from os import path
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template,request,flash,redirect
from flask_login import mixins
app = Flask(__name__)   

app.secret_key="blue red green k"

db = SQLAlchemy(app)
DB_NAME="Users.db"
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
class User(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    First_name=db.Column(db.String(255),nullable=False)
    Last_name=db.Column(db.String(255),nullable=False)
    Email=db.Column(db.String(255),nullable=False, unique=False)
    Password=db.Column(db.String(255),nullable=False)

Specialchar=['$', '@', '#', '%','_']

@app.route('/',methods=['GET','POST'])
def index():
    create_database(app)
    if request.method=='POST':
        FirstName=request.form.get('First_Name')
        LastName=request.form.get('Last_Name')
        Email=request.form.get('email')
        Password=request.form.get('password')
        user = User.query.filter_by(Email=Email).first()
        if user:
            flash('Email already exists.', category='error')
        if len(Password)<8:
            flash('the password must be more than 8 characters',category="error")
        if not any(char.isdigit() for char in Password):
            flash('the password must contain at least one digit',category="error") 
        if not any(char.isupper() for char in Password):
            flash('the password must contain at least one capital letter',category="error") 
        if not any(char in Specialchar for char in Password):
            flash('the password must contain at least one special character such as $,_,@,#,%',category="error") 
        else:
            new_user=User(First_name=FirstName,Last_name=LastName,Email=Email,Password=generate_password_hash(Password,method='sha256'))   
            db.session.add(new_user)
            db.session.commit()
            flash('Account created successfully',category="success")
    return render_template("Sign-Up.html")

    
@app.route('/Login',methods=['GET','POST'])
def login(): 
    #if request.method=='POST':
     #   FirtstName=request.form.get('First_Name')
      #  LastName=request.form.get('Last_Name')
       # Email=request.form.get('email')
       # Passowrd=request.form.get('Password')
       # if len(Passowrd)<8:
        #    flash('the password must be more than 8 characters',category="error")
    return render_template('Login.html')
def create_database(app):
    if not path.exists('/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')
if __name__=="__main__":
    app.run(debug=True)
    

    



        