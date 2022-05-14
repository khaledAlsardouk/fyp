# # import json
# # from os import path
# # from sqlalchemy import  false,true
# # from werkzeug.security import generate_password_hash, check_password_hash
# # from flask_sqlalchemy import SQLAlchemy
# from flask import Flask, render_template,request,flash,redirect, url_for
# from flask_login import UserMixin, user_logged_in
# from flask_login import LoginManager,login_user, login_required, logout_user, current_user
# app = Flask(__name__)   
# app.secret_key="blue red green k"
# login_manager = LoginManager()
# login_manager.login_view = 'login'
# login_manager.init_app(app)

# db = SQLAlchemy(app)
# DB_NAME="Users.db"
# app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
# class User(db.Model,UserMixin):
#     id=db.Column(db.Integer,primary_key=True)
#     First_name=db.Column(db.String(255),nullable=False)
#     Last_name=db.Column(db.String(255),nullable=False)
#     Email=db.Column(db.String(255),nullable=False, unique=False)
#     Password=db.Column(db.String(255),nullable=False)
#     def to_json(self):        
#         return {
#                 "Email": self.Email,
#                 "password":self.Password}
                

#     def is_authenticated(self):
#         return true

#     def is_active(self):   
#         return true           

#     def is_anonymous(self):
#         return False          

#     def get_id(self):         
#         return str(self.id)

# Specialchar=['$', '@', '#', '%','_']

# @app.route('/',methods=['GET','POST'])
# def index():
#     print("signin")
    
#     create_database(app)
#     if request.method=='POST':
#         FirstName=request.form.get('First_Name')
#         LastName=request.form.get('Last_Name')
#         Email=request.form.get('email')
#         Password=request.form.get('password')
#         user = User.query.filter_by(Email=Email).first()
#         if user ==User():
#             flash('Email already exists.', category='error')
#         elif len(Password)<5:
#             flash('the password must be more than 8 characters',category="error")
#         elif not any(char.isdigit() for char in Password):
#             flash('the password must contain at least one digit',category="error") 
#         elif not any(char.isupper() for char in Password):
#             flash('the password must contain at least one capital letter',category="error") 
#         elif not any(char in Specialchar for char in Password):
#             flash('the password must contain at least one special character such as $,_,@,#,%',category="error") 
#         else:
#             new_user=User(First_name=FirstName,Last_name=LastName,Email=Email,Password=generate_password_hash(Password,method='sha256'))   
#             db.session.add(new_user)
#             db.session.commit()
            
#             flash('Account created successfully',category="success")
#             login_user(user,remember=False)
#             return redirect(url_for("home"))
#     return render_template("Sign-Up.html")

    
# @app.route('/Login',methods=['GET','POST'])
# def login(): 
#     print (db)
#     print("hello world3")
#     if request.method == 'POST':
#         print("hello there")
#         email = request.form.get('email')
#         print("hello there")
#         password = request.form.get('passwords')
#         user = User.query.filter_by(Email=email).first()
#         if user:
#            if check_password_hash(user.password,password):
#                 print("hi ")
#                 flash('Logged in successfully!', category='success')
#                 print("hello there2")
#                 login_user(user, remember=false)
#                 return redirect(url_for('home'))
#            else:
               
#                 flash('Incorrect password or email, try again.', category='error')
#                 print("hello there")
#         else:
            
#          return render_template("Login.html", user=current_user)

# @app.route('/home',methods=['GET', 'POST'])
# def home():
    
#     return render_template('home.html')
# @app.route('/logout')
# #@login_required
# #def logout():
#  #   logout_user()
#   #  return redirect(url_for('login'))
# def create_database(app):
    
#     if not path.exists('/' + DB_NAME):
#         db.create_all(app=app)
#         print('Created Database!')
# login_manager = LoginManager()
# login_manager.login_view = 'login'
# login_manager.init_app(app)
# @login_manager.user_loader

# def load_user(id):
#     return User.query.get(int(id))


# if __name__=="__main__":
    
#     app.run(debug=true)
# *#
    

    



        