import smtplib
import os
from email.message import EmailMessage

def sender_detail_exception(senderemail,senderpassword,senderserver):
	try:
		smtp=smtplib.SMTP_SSL(senderserver,465)
		smtp.login(senderemail,senderpassword)
		smtp.quit()
	except Exception as e:
		return str(e)
	else:
		return "Data Saved."
