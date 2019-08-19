simple_message_needs= {"message_category":True,"slack":True,"slackReport":True,"slackChannels":True,"message_type":True,"highlight":True,"email":True}
Notification_message_needs={"message_category":True,"slack":True,"message_type":True,"email":True}

URL = 'http://176.9.137.77/hr_tms/ReactReduxHR/backend/attendance/API_HR/api.php'
URL_details = 'http://176.9.137.77/hr_tms/ReactReduxHR/backend/attendance/sal_info/api.php'


default={
            "monthly_remainder":"Slack_id: Please create your monthly report of :Month till 10th of this month. Failing to do so will automatically set your monthly review to 0.",
            "weekly_remainder1":"Slack_id: you need to create your weekly",
            "weekly_remainder2":"Slack_id: You are past due your date for weekly report, you need to do your weekly report before Thursday. Failing to do so will automatically set your weekly review to 0 which will effect your overall score.",
            "review_activity":"Slack_id: you have weekly report's pending to be reviewed",
            "monthly_manager_reminder":"Slack_id: you have monthly report's pending to be reviewed",
            "missed_checkin":"Slack_id: you have missed Date: checkin",
            "monthly_report_mesg":"Slack_id: your monthly report is reviewed by :Manager_name",
            "weekly_report_mesg":"Slack_id: your weekly report is reviewed by :Manager_name",
            "weekly_report_notes":"Slack_id: your weekly report is skipped by :Manager_name",
            "missed_reviewed_mesg":"Slack_id: you have Reports: weekly report's pending to be reviewed before current week."
            }

mail_settings = {
    "MAIL_SERVER": 'smtp.gmail.com',
    "MAIL_PORT": 465,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": Mail_user,
    "MAIL_PASSWORD": Mail_password
}


checkin_score_scheduler_seconds = 90

overall_score_scheduler_hour = 16
overall_score_scheduler_min = 30

reset_cron_scheduler_hour =18
reset_cron_scheduler_min = 10

missed_checkin_scheduler_hour =11
missed_checkin_scheduler_min =30

weekly_remainder_scheduler_hour=13
weekly_remainder_scheduler_min=2

review_activity_scheduler_hour =12
review_activity_scheduler_min =30

disable_user_scheduler_hour=20
disable_user_scheduler_min=30

monthly_score_scheduler_hour=13
monthly_score_scheduler_min=10

monthly_remainder_scheduler_hour=15
monthly_remainder_scheduler_min=45

monthly_manager_reminder_scheduler_hour=14
monthly_manager_reminder_scheduler_min=30

missed_review_activity_scheduler_hour=12
missed_review_activity_scheduler_min=56