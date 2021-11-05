import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplicationm
  
# list of email_id to send the mail
to = ["rajnishsingh04012001@gmail.com","govinddeshmukh2001@gmail.com"] # the list of the recivers
senderEmail="rajnishsingh1080@gmail.com" #email of the senders
senderPassword="Rajnish@123" #email password od the sender

message=MIMEMultipart("alternative")
message["Subject"]="The test of the task"
message["From"]=senderEmail

html='''<!DOCTYPE html>
<html>
    <body>
        <h1 style="color:SlateGray;">This is an HTML Email!</h1>
    </body>
</html>
'''
htmlmessage=MIMEText(html,"html")
message.attach(htmlmessage)

with open("labass10_8085_488.pdf","rb") as f:
    file_data=f.read()
    file_name=f.name
    print("data: done")
    print("name: done")
    attchment=MIMEApplication(file_data,"pdf")
    message.attach(attchment)

s = smtplib.SMTP('smtp.gmail.com', 587)
s.starttls()
s.login(senderEmail, senderPassword)

s.sendmail(senderEmail, to, message.as_string())
s.quit()

print("message send")