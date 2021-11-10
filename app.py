from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from flask_sqlalchemy  import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
#rajnish libarary added
import json
import pandas as pd
import os
from sendEmail.SENDEmail import addEmails, addContent, mail_send_by_flask, good_content
import requests



app = Flask(__name__)
app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/hp/Desktop/bulkmail/database.db'
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# this is rajnish
with open("config.json", "r") as parameters:
    params=json.load(parameters)["params"]

with open("config.json", "r") as parameters:
    errors=json.load(parameters)["errors"]

#end of my code


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')

class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('dashboard'))

        return '<h1>Invalid username or password</h1>'
        #return '<h1>' + form.username.data + ' ' + form.password.data + '</h1>'

    return render_template('login.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return '<h1>New user has been created!</h1>'
        #return '<h1>' + form.username.data + ' ' + form.email.data + ' ' + form.password.data + '</h1>'

    return render_template('signup.html', form=form)

@app.route('/dashboard')
@login_required
def dashboard():
    params["username"]=current_user.username
    return render_template('dashboard.html',params=params)

@app.route('/dashboard/sender', methods= ['GET','POST']) 
def senderemail():
    if request.method =="POST":
        params["senderEmail"]=request.form.get("sender-email")
        params["senderPassword"]=request.form.get("sender-password")
        params["senderServer"]=request.form.get("sender-server")
        if params["senderServer"] == "":
            params["senderServer"]="smtp.gmail.com"
        print(params["senderEmail"],params["senderPassword"],params["senderServer"])
    return render_template('dashboard.html',params=params)

@app.route('/dashboard/mails', methods = ['GET','POST'])
def emailer():
    if request.method =="POST":
        f=request.files['emails']
        df=pd.read_excel(f)
        list=[]
        for x in df['email']:
            list.append(x)
        params["reciversEmail"]=addEmails(list)
        print(params["reciversEmail"])
    return redirect(request.referrer)

@app.route('/dashboard/htmlContent', methods = ['GET','POST'])
def mailer():
    if request.method == "POST":
        params["subject"]=request.form.get("subject")
        print(params["subject"])
        f=request.files['html-text']
        dff = f.read()
        dff=dff.decode("utf-8")

        params["mailContent"]=dff
    return redirect(request.referrer)

@app.route('/dashboard/sendmail')
def mailsend():
    reciverEmails = str(params["reciversEmail"])
    senderEmail=str(params["senderEmail"])
    senderPassword=str(params["senderPassword"])
    subject=str(params["subject"])
    server = str(params["senderServer"])
    string=str(params["mailContent"])
    mess = mail_send_by_flask(senderEmail,senderPassword,reciverEmails,subject,server,string)
    return mess 

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
