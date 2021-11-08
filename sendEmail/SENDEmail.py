import smtplib
import os
from email.message import EmailMessage
import pathlib
'''
senderEmail=""     # email of the sender
senderPassword=""  # password of the email by which wanted to send mail		#creation of smpt_ssl server to send email
 #string of recivers emails
message=None   #email message veriable created
'''

# this function set the value of the sender email and password
# login into the email by which you wanted to send mail




#this function is used to create a string of list of emails
# the return type is string
# the param is a list of emails
def addEmails(email):
	global reciverEmials
	reciverEmials="rajnishsingh04012001@gmial.com"
	for x in email:
		reciverEmials=reciverEmials+", "+x
	return reciverEmials


def addContent(string, main_type, sub_type):
	global message
	data = None
	try:
		message=EmailMessage()
		if(main_type == "path"):
			data = open(string).read()
			if(sub_type=="text"):
				message.set_content(data)
			if(sub_type == "html"):
				message.set_content("")
				message.add_alternative(data,subtype='html')
		elif(main_type=="text"):
			if(sub_type=="text"):
				message.set_content(string)
			if(sub_type == "html"):
				message.set_content("")
				message.add_alternative(string,subtype='html')
	except:
		return "error"
	else:
		return message

def addAttachment(path):
	with open(path,"rb") as file:
		filesname=file.name
		file_type=pathlib.Path(path).suffix # to get the file extenction
		file_data=file.read()
	message.add_attachment(file_data,maintype="application",subtype=file_type,filename=filesname)
	return "FILE ATTCHED NO ERROR"


def sendEmail(senderemail,senderpassword, subject, reciverEmials):
	message["Subject"]=subject
	message["From"]=senderemail
	message["To"]=reciverEmials
	try:
		with smtplib.SMTP_SSL("smtp.gmail.com",465) as smtp:
			smtp.login(senderemail,senderpassword)
			smtp.send_message(message)
	except:
		print("error occurred")
	else:
		return "MESSAGE SEND"

def mail_send_by_flask(senderemail,senderpassword,reciverEmials,subject,server,string):
	try:
		message=EmailMessage()
		message.set_content("no content")
		message.add_alternative(string,subtype='html')

		message["Subject"]=subject
		message["From"]=senderemail
		message["To"]=reciverEmials
	except Exception as e:
		 print("error1",e)
		 return "error1"

	try:
		with smtplib.SMTP_SSL("smtp.gmail.com",465) as smtp:
			smtp.login(senderemail,senderpassword)
			smtp.send_message(message)
	except Exception as e:
		 print("error2",e)
		 return "error2"
	else:
		return "MESSAGE SEND"

def good_content(string):
	bad_words=["\n","\t","\r","\a"]
	for i in bad_words :
		string = string.replace(i, "")
	print(string)
	return string


