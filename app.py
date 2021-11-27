from flask import Flask, render_template, redirect, url_for, request, flash, session, jsonify
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
from sendEmail.SENDEmail import addEmails, addContent, mail_send_by_flask, good_content,solveit
import requests
from sendEmail.exception_handle import *



app = Flask(__name__)
app.secret_key="MagamInfoTech"
app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
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

        return redirect(url_for('login'))
        #return '<h1>' + form.username.data + ' ' + form.email.data + ' ' + form.password.data + '</h1>'

    return render_template('signup.html', form=form)
# every time i wanted to pass the obect of think i wnated to show only.
@app.route('/dashboard')
@login_required
def dashboard():
    p={}
    p["userName"]=current_user.username
    p["reciversEmail"]="No Email"
    p["senderEmail"]="asd"
    p["senderServer"]="qwer"
    p["senderPassword"]=""
    p["subject"]=""
    p["mailContent"]=""
    p["saveError"]=""
    p["emailError"]=""
    p["messageError"]=""
    p["sendError"]=""
    p["emailData"]=""
    p["placeholderServer"]="smtp.gmail.com"
    p["placeholderEmail"]="asdf@gmail.com"
    p["placeholderPassword"]="Password"
    return render_template('dashboard.html',p=p)

@app.route('/dashboard/sender', methods= ['GET','POST']) 
def senderemail():
    if request.method =="POST":
        p2={}
        p2["senderEmail"]=request.form.get("sender-email")
        p2["senderPassword"]=request.form.get("sender-password")
        p2["senderServer"]=request.form.get("sender-server")
        p2["placeholderServer"]=p2["senderServer"]
        p2["placeholderEmail"]=p2["senderEmail"]
        p2["placeholderPassword"]=p2["senderPassword"]
        if p2["senderServer"] == "":
            p2["senderServer"]="smtp.gmail.com"
        #print(p2["senderEmail"],p2["senderPassword"],p2["senderServer"])
        p2["saveError"]="<h4>"+sender_detail_exception(p2["senderEmail"],p2["senderPassword"],p2["senderServer"])+ "</h4>"
    return render_template('dashboard.html', p=p2)

@app.route('/dashboard/mails', methods = ['GET','POST'])
def emailer():
    p={}
    if request.method =="POST":
        
        #print("came in out1")
        f=request.files['emails']
        if f.filename == '':
            flash('No selected file')
            return redirect(request.url)
        #print("came in out2")
        if f.filename.split('.')[1] != "xlsx":
            #print("came in out3")
            #print(f.filename.split('.')[1])
            p["emailError"]="<h4>The input file is not .xlsx</h4>"
            return render_template('dashboard.html',p=p)  
        p["emailData"]=f.filename
        df=pd.read_excel(f)

        if "email" not in df.columns:
            #print("came in out4")
            p["emailError"]="<h4>File not have column name 'email' </h4>"
            return render_template('dashboard.html',p=p)
        list=[]
        for x in df['email']:
            list.append(x)
        p["reciversEmail"]=addEmails(list)
        del list
        #print(p["reciversEmail"])
    #return redirect(request.referrer)
    p["emailError"]=""
    return render_template('dashboard.html', p=p)

@app.route('/dashboard/htmlContent', methods = ['GET','POST'])
def mailer():
    p={}
    if request.method == "POST":
        p["subject"]=request.form.get("subject")

        p["editor"]=request.form.get("editor")
        if p["subject"]=="":
            p["messageError"]="<h4>Plaeas add an subject to to send mail</h4>"
            return render_template('dashboard.html',p=p)
        #print(p["subject"])
        #print(p["editor"])
        f=request.files['html-text']
        if f.filename == '' and p["editor"]=="":
            flash('No selected file')
            return redirect(request.url)
        if f.filename == '' and p["editor"]!="":
            p["mailContent"]=p["editor"]
            p["messageError"]="<h4>message added</h4>"
            
        if f.filename != '' and p["editor"]=="":
            dff = f.read()
            dff=dff.decode("utf-8")
            p["mailContent"]=dff
            p["messageError"]="<h4>message added</h4>"
            
        if f.filename != '' and p["editor"]!="":
            dff = f.read()
            dff=dff.decode("utf-8")
            p["mailContent"]=dff
            p["messageError"]="<h4>message added</h4>"
            

    #return redirect(request.referrer)
    return render_template('dashboard.html',p=p)

@app.route('/dashboard/sendmail', methods = ['GET','POST'])
def mailsend():
    p={}
    if request.method == "POST":
        server = request.form.get("sendserverqwer")
        senderEmail=request.form.get("sendemailqwer")
        senderPassword=request.form.get("sendpasswordqwer")
        reciverEmails=request.form.get("sendreciveremailqwer")
        subject = request.form.get("sendsubjectqwer")
        string=request.form.get("sendmessageqwer")
        #print(server)
        #print(senderEmail)
        #print(senderPassword)
        #print(reciverEmails)
        #print(subject)
        #print(string)
        p["sendError"] = mail_send_by_flask(senderEmail,senderPassword,reciverEmails,subject,server,string)
        p["subject"]=""
        p["mailContent"]=""
        p["emailError"]=""
        p["messageError"]=""
        p["emailData"]=""
        return render_template('dashboard.html',p=p) 
    else:
        flash('no post request')
        return redirect(request.url)




@app.route('/dashboard/sendmailcc', methods = ['GET','POST'])
def mailsendupto():
    p={}
    if request.method == "POST":
        server = request.form.get("sendserverqwer2")
        senderEmail=request.form.get("sendemailqwer2")
        senderPassword=request.form.get("sendpasswordqwer2")
        reciverEmails=request.form.get("sendreciveremailqwer2")
        subject = request.form.get("sendsubjectqwer2")
        string=request.form.get("sendmessageqwer2")
        #print(server)
        #print(senderEmail)
        #print(senderPassword)
        #print(reciverEmails)
        #print(subject)
        #print(string)
        p["sendError"] = solveit(senderEmail,senderPassword,reciverEmails,subject,server,string)
        p["subject"]=""
        p["mailContent"]=""
        p["emailError"]=""
        p["messageError"]=""
        p["emailData"]=""
        return render_template('dashboard.html',p=p) 
    else:
        flash('no post request')
        return redirect(request.url)
    

'''
@app.route("/logoutdata")
def logoutdata():
  session['Username'] = flask.request.args.get('Username')
  print("the username is:")
  print(session['Username'])
  return flask.jsonify({'success':'True'})   
'''
@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    if request.method == "POST":
        print(request.form.get("logout"))
    logout_user()
    #print("hear")
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
