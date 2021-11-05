from flask import Flask, request, render_template, redirect
import json
import pandas as pd
import os
from sendEmail.SENDEmail import addEmails

with open("config.json", "r") as parameters:
    params=json.load(parameters)["params"]


app = Flask(__name__)  


@app.route('/')  
def upload():  
    return render_template("index.html",sendermail=params["senderEmail"],sendermailpassword=params["senderPassword"]) 


@app.route('/sender-email', methods= ['GET','POST']) 
def senderemail():
    if request.method =="POST":
        params["senderEmail"]=request.form.get("sender-email")
        params["senderPassword"]=request.form.get("sender-password")    
    return render_template("index.html",sendermail=params["senderEmail"],sendermailpassword=params["senderPassword"])  


@app.route('/mails', methods = ['GET','POST'])
def emailer():
    if request.method =="POST":
        f=request.files['emails']
        df=pd.read_excel(f)
        list=[]
        for x in df['email']:
            list.append(x)
        params["reciversEmail"]=addEmails(list)
    return redirect(request.referrer)

@app.route('/htmlContent', methods = ['GET','POST'])
def mailer():
    if request.method == "POST":
        f=request.files['html-text']
        text = f.read()
    return redirect(request.referrer)

     
    

 
  
if __name__ == '__main__':  
    app.run(debug = True)