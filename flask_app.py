from flask import Flask, request, render_template, redirect
import json
import pandas as pd
import os
from sendEmail.SENDEmail import addEmails, addContent, mail_send_by_flask, good_content
import requests

with open("config.json", "r") as parameters:
    params=json.load(parameters)["params"]


app = Flask(__name__)  


@app.route('/')  
def upload():  
    return render_template("index2.html",params=params) 


@app.route('/sender', methods= ['GET','POST']) 
def senderemail():
    if request.method =="POST":
        params["senderEmail"]=request.form.get("sender-email")
        params["senderPassword"]=request.form.get("sender-password")
        params["senderServer"]=request.form.get("sender-server")
        if params["senderServer"] == "":
            params["senderServer"]="smtp.gmail.com"
        print(params["senderEmail"],params["senderPassword"],params["senderServer"])
    return render_template("index2.html",params= params)  


@app.route('/mails', methods = ['GET','POST'])
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

@app.route('/htmlContent', methods = ['GET','POST'])
def mailer():
    if request.method == "POST":
        params["subject"]=request.form.get("subject")
        print(params["subject"])
        f=request.files['html-text']
        dff = f.read()
        dff=dff.decode("utf-8")

        params["mailContent"]=dff
    return redirect(request.referrer)

     
@app.route('/sendmail')
def mailsend():
    reciverEmails = str(params["reciversEmail"])
    senderEmail=str(params["senderEmail"])
    senderPassword=str(params["senderPassword"])
    subject=str(params["subject"])
    server = str(params["senderServer"])
    string=str(params["mailContent"])
    mess = mail_send_by_flask(senderEmail,senderPassword,reciverEmails,subject,server,string)
    return mess 
 

 
  
if __name__ == '__main__':  
    app.run(debug = True)