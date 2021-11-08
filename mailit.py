from sendEmail.SENDEmail import addEmails, addContent, addAttachment, sendEmail, mail_send_by_flask
'''
email = ["rajnishsinghwork@gmail.com", "488_bt19@iiitkalyani.ac.in"]
print(addEmails(email))
print(addContent("./testmail/index.html","path","html"))
print(addAttachment("F:/56495.jpg"))
print(sendEmail("rajnishsingh1080@gmail.com", "Rajnish@123", "the test message"))


'''
email = ["rajnishsinghwork@gmail.com", "488_bt19@iiitkalyani.ac.in"]
reciverEmails = addEmails(email)
senderEmail="rajnishsingh1080@gmail.com"
senderPassword="Rajnish@123"
subject="the flak app3"
server = "smtp.gmail.com"
f = open("./testmail/index.html").read()
string=str(f)
mail_send_by_flask(senderEmail,senderPassword,reciverEmails,subject,server,string)



'''
import smtplib
import os
from email.message import EmailMessage
import pathlib


# globel variable which we will be using
reciverEmials = "rajnishsingh04012001@gmail.com, 488_bt19@iiitkalyani.ac.in" # the list of the recivers (comma seperated email addresses)
senderEmail="rajnishsingh1080@gmail.com" #email of the senders
senderPassword="Rajnish@123" #email password od the sender
emailSubject=" the thin is a subject"
messageInText="done it by new methord"
emailHtmlPath="index.html"
emailAttachmentPath="F:/56495.jpg"
emailCode="233#$dfr$%5"



def send_email():
    message=EmailMessage()
    # to add details.
    message["Subject"]=emailSubject
    message["From"]=senderEmail
    message["To"]=reciverEmials

    # to add text
    message.set_content(messageInText)

    # to add html file
    html_message=open(emailHtmlPath).read()
    message.add_alternative(html_message,subtype='html')

    # to add the attachments pdf doc png jpg xlxs and etc i can always send dem as an application
    with open(emailAttachmentPath,"rb") as file:
        file_name=file.name
        file_type=pathlib.Path(emailAttachmentPath).suffix # to get the file extenction
        file_data=file.read()
    message.add_attachment(file_data,maintype="application",subtype=file_type,filename=file_name)

    with smtplib.SMTP_SSL("smtp.gmail.com",465) as smtp:
        smtp.login(senderEmail,senderPassword)
        smtp.send_message(message)
    print("message send")

send_email()
'''