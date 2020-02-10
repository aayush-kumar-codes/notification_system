import os
import sys    
import random
import re
from app import mongo
from app.util import serialize_doc
import datetime
import dateutil.parser
from bson.objectid import ObjectId
from app.mail_util import send_email,validate_smtp_counts,validate_smtp
from app.slack_util import slack_message
from flask import current_app as app
from dotenv import load_dotenv
import uuid
import time
import imapclient
import pyzmail
import email


def campaign_mail():
    APP_ROOT = os.path.join(os.path.dirname(__file__), '..')
    dotenv_path = os.path.join(APP_ROOT, '.env')
    load_dotenv(dotenv_path)
    campaigns = mongo.db.campaigns.find({"status":"Running"})
    campaigns = [serialize_doc(doc) for doc in campaigns]
    
    for campaign in campaigns:
        if campaign is not None:
            message_subject_details = []
            if 'message_detail' in campaign:
                if campaign['message_detail']:
                    highest_count_message = max(campaign['message_detail'], key=lambda x:x['count'])
                    for message_detail in campaign['message_detail']:
                        if message_detail['count'] == highest_count_message['count']:
                            message_subject_details.append(message_detail)
                    
            filelink = None
            if 'attachment_file_name' in campaign:
                filelink = campaign['attachment_file']
            filename = None
            if 'attachment_file' in campaign:
                filename = campaign['attachment_file_name']

            campaign_users = mongo.db.campaign_users.find({"campaign":campaign['_id']})
            campaign_users = [serialize_doc(doc) for doc in campaign_users]
            total_users = 0
            for user in campaign_users:
                if user is not None: 
                    status = mongo.db.campaign_users.find_one({"_id":ObjectId(user['_id'])})
                    if status['block'] is False and status['mail_cron'] is False:
                        try:
                            validate = validate_smtp_counts(campaign['smtps'])
                        except Exception as error:
                            campaign_status_err = mongo.db.campaigns.update({"_id":ObjectId(campaign['_id'])},
                                    {
                                        "$set": {
                                                "status": repr(error)
                                            }
                                    })
                            return None
                        else:
                            mail_server = validate['mail_server']
                            mail_port = validate['mail_port']
                            mail_username = validate['mail_username']
                            mail_password = validate['mail_password']
                            count_details = validate['count_details']
                            final_message = random.choice(message_subject_details)
                            mail = user['email']
                            if os.getenv('ENVIRONMENT') == "development":
                                mail = os.getenv('to')
                            unique = str(user['_id'])
                            
                            system_variable = mongo.db.mail_variables.find({})
                            system_variable = [serialize_doc(doc) for doc in system_variable]
                            subject = final_message['message_subject']
                            message_variables = []
                            message = final_message['message'].split('#')
                            del message[0]
                            rex = re.compile('!|@|\$|\%|\^|\&|\*|\:|\;')
                            for elem in message:
                                varb = re.split(rex, elem)
                                message_variables.append(varb[0])
                            message_str = final_message['message']
                            for detail in message_variables:
                                if detail in campaign:
                                    rexWithString = '#' + re.escape(detail) + r'([!]|[@]|[\$]|[\%]|[\^]|[\&]|[\*]|[\:]|[\;])'
                                    message_str = re.sub(rexWithString, campaign[detail], message_str)
                                elif detail in user:
                                    rexWithString = '#' + re.escape(detail) + r'([!]|[@]|[\$]|[\%]|[\^]|[\&]|[\*]|[\:]|[\;])'
                                    message_str = re.sub(rexWithString, user[detail], message_str)
                                else:
                                    for element in system_variable:
                                        if "#" + detail == element['name'] and element['value'] is not None:
                                            rexWithSystem = re.escape(element['name']) + r'([!]|[@]|[\$]|[\%]|[\^]|[\&]|[\*]|[\:]|[\;])' 
                                            message_str = re.sub(rexWithSystem, element['value'], message_str)  
                            subject_variables = []
                            message_sub = subject.split('#')
                            del message_sub[0]
                            regex = re.compile('!|@|\$|\%|\^|\&|\*|\:|\;')
                            for elem in message_sub:
                                sub_varb = re.split(regex, elem)
                                subject_variables.append(sub_varb[0])
                            message_subject = subject
                            for detail in subject_variables:
                                if detail in campaign:
                                    rexWithString = '#' + re.escape(detail) + r'([!]|[@]|[\$]|[\%]|[\^]|[\&]|[\*]|[\:]|[\;])'
                                    message_subject = re.sub(rexWithString, ret[detail], message_subject)
                                elif detail in user:
                                    rexWithString = '#' + re.escape(detail) + r'([!]|[@]|[\$]|[\%]|[\^]|[\&]|[\*]|[\:]|[\;])'
                                    message_str = re.sub(rexWithString, ret[detail], message_str)
                                else:
                                    for element in system_variable:
                                        if "#" + detail == element['name'] and element['value'] is not None:
                                            rexWithSystem = re.escape(element['name']) + r'([!]|[@]|[\$]|[\%]|[\^]|[\&]|[\*]|[\:]|[\;])' 
                                            message_subject = re.sub(rexWithSystem, element['value'], message_subject)  
                    
                            digit = str(uuid.uuid4())
                            to = []
                            to.append(mail)
                            working_status = True
                            # try:        
                            send_email(message=message_str,
                            recipients=to,
                            subject=message_subject,
                            user=unique,
                            campaign=str(campaign['_id']),
                            sending_mail= mail_username,
                            sending_password= mail_password,
                            sending_server= mail_server,
                            digit=digit,
                            campaign_message_id=final_message['message_id'],
                            filelink=filelink,
                            filename=filename,
                            sending_port= mail_port)
                            # except Exception as error:
                            #     if total_users == 3:
                            #         error = mongo.dbsd.campaigns.update({"campaign_id": campaign['_id']},{
                            #             "$pull":{
                            #                 "smtps": mail_server
                            #             }

                            #         })
                            #         return None
                            #     else:
                                #     total_users +=1
                                #     campaing_user_failed = mongo.db.campaign_users.update({"_id":ObjectId(user['_id'])},
                                #     {
                                #         "$set": {
                                #                 "send_status": True,
                                #                 "mail_cron": True,
                                #                 "successful":  working_status,
                                #                 "error_message" : repr(error),
                                #                 "error_time": datetime.datetime.now(),
                                            
                                #         }
                                #     })

                                # working_status = False   
                            # else:  
    
                            mail_data = mongo.db.mail_status.insert_one({
                                "user_mail": user['email'],
                                "user_id": str(user['_id']),
                                "sending_time": datetime.datetime.utcnow(),
                                "message": message_str,
                                "mail_sended_status": working_status,
                                "subject":message_subject,
                                "recipients": to,
                                "digit": digit,
                                "campaign": str(campaign['_id']),
                                "sending_mail": mail_username,
                                "sending_password":mail_password,
                                "sending_server":mail_server,
                                "seen": False,
                                "sending_port":mail_port,
                                "clicked": False

                            }).inserted_id
                            smtp_val = mongo.db.smtp_count_validate.update({"_id": ObjectId(count_details)},{
                                "$inc": {
                                    "count": 1
                                    }
                            })

                            user_status = mongo.db.campaign_users.update({"_id":ObjectId(user['_id'])},
                                {
                                    "$set": {
                                            "send_status": True,
                                            "mail_cron": True,
                                            "successful":  working_status,
                                            "sended_date": datetime.datetime.now(),
                                    },
                                        "$push": {
                                            "mail_message": {
                                            "sended_message_details": digit,
                                            "campaign": str(campaign['_id'])
                                        }
                                    }
                                })
                            
                            # finding if campaign have no user left which mail is needed to be send mark it as completed
                            user_available = mongo.db.campaign_users.aggregate([{ "$match" : {"campaign":campaign['_id']}},{ "$group": { "_id": None, "count": { "$sum": 1 } } }])
                            user_available = [serialize_doc(doc) for doc in user_available]

                            user_completed = mongo.db.campaign_users.aggregate([{ "$match" : {"campaign":campaign['_id'],"send_status":True,"mail_cron":True}},{ "$group": { "_id": None, "count": { "$sum": 1 } } }])
                            user_completed = [serialize_doc(doc) for doc in user_completed]
                            
                            for data in user_available:
                                for element in user_completed:
                                    if data['count'] == element['count']:
                                        campaign_status = mongo.db.campaigns.update({"_id":ObjectId(campaign['_id'])},
                                            {
                                                "$set": {
                                                        "status": "Completed"
                                                    }
                                            })
                                    else:
                                        pass
                            time.sleep(campaign['delay'])
                    else:
                        pass
                else:
                    pass
        else:
            pass
                
def calculate_bounce_rate():
    campaigns = mongo.db.campaigns.find({"status":"Running"})
    campaigns = [serialize_doc(doc) for doc in campaigns]
    
    for campaign in campaigns:
        if campaign is not None:
            campaign_users = mongo.db.campaign_users.find({"campaign":campaign['_id']})
            campaign_users = [serialize_doc(doc) for doc in campaign_users]
            bounce = mongo.db.bounce_emails.find({})
            bounce = [serialize_doc(doc) for doc in bounce]
            bounce_users = []
            total_users = len(campaign_users)
            for user in campaign_users:
                for data in bounce:
                    if user['email'] == data['bounced_mail'] and data['bounce_type'] == "hard":
                        if user['email'] not in bounce_users:
                            bounce_users.append(user['email'])
            bounce_rate = len(bounce_users) *100 / total_users
            campaign = mongo.db.campaigns.update({"_id": ObjectId(campaign['_id'])},{
                "$set": {
                    "bounce_rate": bounce_rate
                }
            })
        else:
            pass

            
def reject_mail():
    ret = mongo.db.rejection_handling.find_one({"send_status":False})
    if ret is not None:
        mail = ret['email']
        message = ret['message']
        time = ret['rejection_time']  
        time_update = dateutil.parser.parse(time).strftime("%Y-%m-%dT%H:%M:%SZ")
        rejected_time = datetime.datetime.strptime(time_update,'%Y-%m-%dT%H:%M:%SZ')
        diffrence = datetime.datetime.utcnow() - rejected_time
        if diffrence.days >= 1:
            to = []
            to.append(mail)
            send_email(message=message,recipients=to,subject='REJECTED')
            user_status = mongo.db.rejection_handling.remove({"_id":ObjectId(ret['_id'])})
        else:
            pass
    else:
        pass

def cron_messages():
    ret = mongo.db.messages_cron.find_one({"cron_status":False,"message_detail.message_origin":"HR"})
    if ret is not None:
        vet = mongo.db.messages_cron.update({"_id":ObjectId(ret['_id'])},
            {
                "$set": {
                        "cron_status": True
                    }
                    })

        if ret['type'] == "email":
            send_email(message=ret['message'],recipients=ret['recipients'],subject=ret['subject'])
        elif ret['type'] == "slack":
            slack_message(message=ret['message'],channel=ret['channel'],req_json=ret['req_json'],message_detail=ret['message_detail'])
        else:
            pass    
    else:
        pass 


def tms_cron_messages():
    ret = mongo.db.messages_cron.find_one({"cron_status":False,"message_detail.message_origin":"TMS"})
    if ret is not None:
        vet = mongo.db.messages_cron.update({"_id":ObjectId(ret['_id'])},
            {
                "$set": {
                        "cron_status": True
                    }
                    })

        if ret['type'] == "email":
            send_email(message=ret['message'],recipients=ret['recipients'],subject=ret['subject'])
        elif ret['type'] == "slack":
            slack_message(message=ret['message'],channel=ret['channel'],req_json=ret['req_json'],message_detail=ret['message_detail'])
        else:
            pass    
    else:
        pass 

def recruit_cron_messages():
    ret = mongo.db.messages_cron.find_one({"cron_status":False,"message_detail.message_origin":"RECRUIT"})
    if ret is not None:
        vet = mongo.db.messages_cron.update({"_id":ObjectId(ret['_id'])},
            {
                "$set": {
                        "cron_status": True
                    }
                    })

        if ret['type'] == "email":
            send_email(message=ret['message'],recipients=ret['recipients'],subject=ret['subject'])
        elif ret['type'] == "slack":
            slack_message(message=ret['message'],channel=ret['channel'],req_json=ret['req_json'],message_detail=ret['message_detail'])
        else:
            pass    
    else:
        pass 