import datetime
import requests
from app import mongo
import smtplib,ssl    
import os 
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import email.mime.application
import mimetypes
<<<<<<< HEAD
from flask import current_app as app
from app.config import smtp_counts


def validate_smtp_counts():
    mail = mongo.db.mail_settings.find({"origin": "CAMPAIGN"}).sort({"priority":-1})
    mail = [serialize_doc(doc) for doc in mail]
    valid_smtp = []
    for data in mail:
        mail_username = data['mail_username']
        mail_password = data['mail_password']
        mail_smtp = data['mail_server']
        mail_port = data['mail_port']
        if mail_smtp in smtp_counts:
            smtp_validate = mongo.db.smtp_count_validate.find_one({"smtp":mail_smtp,"email":mail_username,"created_at":datetime.date.today()})
            if smtp_validate is not None:
                if smtp_validate['count'] < smtp_counts[mail_smtp]:
                    valid_smtp.append({"mail_username":mail_username,"mail_password":mail_password,"mail_server":mail_smtp,"mail_port":mail_port})
                else:
                    valid_smtp.append({"Working":False})
        else:
            valid_smtp.append({"unactive":mail_smtp})


    return valid_smtp


def send_email(message,recipients,subject,bcc=None,cc=None,filelink=None,filename=None,link=None,sending_mail=None,sending_password=None,sending_port=None,sending_server=None,template_id=None):
=======
from app.config import base_url
from dotenv import load_dotenv
import uuid

def send_email(message,recipients,subject,bcc=None,cc=None,filelink=None,filename=None,link=None,sending_mail=None,sending_password=None,sending_port=None,sending_server=None,template_id=None,user=None):
    APP_ROOT = os.path.join(os.path.dirname(__file__), '..')
    dotenv_path = os.path.join(APP_ROOT, '.env')
    load_dotenv(dotenv_path)
>>>>>>> 9f326339cb05a5cca115142acb7d1c09faa8b21c
    # again below checking origin condition as this function sends mail so need to check and select right smtp for single mail sending
    if os.getenv('origin') == "hr":
        mail_details = mongo.db.mail_settings.find_one({"origin": "HR"},{"_id":0})
    elif os.getenv('origin') == "recruit":    
        mail_details = mongo.db.mail_settings.find_one({"origin": "RECRUIT"},{"_id":0})
    username = None
    if sending_mail is None:    
        username = mail_details["mail_username"]
    else:
        username = sending_mail 
    password = None
    #below is written for recruit condition for multiple smtp as need to iterate over values from campaign schduler
    if sending_password is None:       
        password = mail_details["mail_password"]
    else:
        password = sending_password   
    if sending_port is None:        
        port = mail_details['mail_port']
    else:
        port = sending_port
    if sending_server is None:        
        mail_server = mail_details['mail_server']
    else:
        mail_server = sending_server  
    context = ssl.create_default_context() 
    if port == 587:       
        mail = smtplib.SMTP(str(mail_server), port)
        mail.ehlo() 
        mail.starttls(context=context) 
        mail.ehlo() 
        mail.login(username,password)
    else:
        mail = smtplib.SMTP_SSL(str(mail_server), port)
        mail.login(username,password)
    delivered = []
    for element in recipients:
        delivered.append(element)
    if bcc is not None:
        for data in bcc:
            delivered.append(data) 
    else:
        bcc = None
    if cc is not None:
        for data in cc:
            delivered.append(data)
        cc =  ','.join(cc)
    else:
        cc = None
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = username
    msg['To'] = ','.join(recipients) 
    msg['Cc'] = cc
    if filelink is not None:
        fo=open(filelink,'rb')
        file = email.mime.application.MIMEApplication(fo.read())
        fo.close()
        file.add_header('Content-Disposition','attachment',filename=filename)
        msg.attach(file)
    else:
        pass
    if template_id is not None:
        if user is not None:
            digit = str(uuid.uuid4())
            url = "<img src= '{}template_hit_rate/{}/{}?template={}&hit_rate=1'>".format(base_url,digit,user,template_id)
            message = message + url 
    main = MIMEText(message,'html')
    msg.attach(main)
    mail.sendmail(username,delivered, msg.as_string()) 
    mail.quit()
    