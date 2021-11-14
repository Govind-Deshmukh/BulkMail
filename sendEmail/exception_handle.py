import smtplib
import os
from email.message import EmailMessage

def sender_detail_exception(senderemail,senderpassword,senderserver):
	try:
		with smtplib.SMTP_SSL("senderserver",465) as smtp:
			try:
				smtp.login(senderemail,senderpassword)
			except:
				return "ERROR in Login rwrong email and password entered."
	except:
		return "the error in server entered try with smtp.gmail.com."

