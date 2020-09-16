rec_templates = [
    {
        "Doc_type" : "email",
        "for" : "when interview first round mail is sent",
        "message" : "Hi #name:, <br/> Thank you for applying for the job #job_profile:. <br/> After reviewing your application, we are excited to move forward with the interview process. <br/> Your First round with #company: has been schedule on #date: at the #venue: for #job_profile: <br/> Do revert back with your availablity for the same. <br/> #hr_signature: ",
        "message_key" : "first_round",
        "message_origin" : "RECRUIT",
        "message_subject" : "#name: your interview for #job_profile: is scheduled",
        "recruit_details" : "Interview First Round",
        "version" : 1,
        "default" : False,
        "working" : True,
        "mobile_message" : "Hi,#name: Your First round with #company: has been schedule on #date: at the #venue: for #job_profile:"
    },
    {
        "Doc_type" : "email",
        "for" : "when candidate is hired",
        "message" : "<p>Dear #name:, <br/> Greetings from #company: <br/>We are pleased to inform you that based on your subsequent interview and application; we are welcoming you to our organization #company: for the position of #job_profile: We look forward to you joining us from #date: at #time:. <br/> Please do not hesitate to call us for any information you may need.<br/>Kindly send your acceptance for the same.<br/> Congratulations! <br/> With Regards,<br/> #hr_signature: </p>",
        "message_key" : "interviewee_selection",
        "message_origin" : "RECRUIT",
        "message_subject" : "Job Offer For #job_profile:",
        "recruit_details" : "Interviewee Selection",
        "version" : 1,
        "default" : True,
        "working" : True,
        "mobile_message" : "Dear #name: We are pleased to inform you that, we have selected you for the position of #job_profile: We look forward to you joining us from #date:.Please do not hesitate to call us for any information you may need Congratulations!With Regards"
    },
    {
        "Doc_type" : "email",
        "for" : "when interview second round mail is sent",
        "message" : "Hi #name:, <br/> Your Second round with #company: has been schedule on #date: at the #venue: for #job_profile: <br/> #hr_signature: ",
        "message_key" : "second_round",
        "message_origin" : "RECRUIT",
        "message_subject" : "#name: your interview for Second round for #job_profile: is scheduled",
        "recruit_details" : "Interview Second Round",
        "version" : 1,
        "default" : True,
        "working" : True,
        "mobile_message" : "Hi #name:, Your Second round with #company: has been schedule on #date: at the #venue: for #job_profile:"
    },
    {
        "Doc_type" : "email",
        "for" : "when interview third round mail is sent",
        "message" : "Hi #name:, <br/> Your Third round with #company: has been schedule on #date: at the #venue: for #job_profile: <br/> #hr_signature: ",
        "message_key" : "third_round",
        "message_origin" : "RECRUIT",
        "message_subject" : "#name: your interview for Third round for #job_profile: is scheduled",
        "recruit_details" : "Interview Third Round",
        "version" : 1,
        "default" : True,
        "working" : True,
        "mobile_message" : "Hi,#name: Your Third round with #company: has been schedule on #date: at the #venue: for #job_profile:"
    },
    {
        "message_key" : "chat_interested",
        "message" : "<p>\n  Hi #name: <br/> Thank you for applying to the #job_profile: position at #company:. If you are interested for the role,kindly reply to this mail and we will contact you on this same email for further details.<br/>#hr_signature:\n</p>",
        "working" : True,
        "message_origin" : "RECRUIT",
        "message_subject" : "#name: Your application for #job_profile:",
        "version" : 1,
        "default" : True,
        "for" : "when candidate is shortlisted",
        "recruit_details" : "still interested?",
        "Doc_type" : "email",
        "mobile_message" : "null"
    },
    {
        "message_key" : "chat_details",
        "message" : "<p>\n  Hi #name: <br> we would love to chat with you regarding #job_profile: from #company: <br/> <br/> Please kindly reply to this email with a suitable time, we would love to have a chat with you \n.<br/>#hr_signature:\n</p>",
        "working" : True,
        "message_origin" : "RECRUIT",
        "message_subject" : "#name: Your application for #job_profile:",
        "version" : 1,
        "default" : False,
        "for" : "when candidate is shortlisted",
        "recruit_details" : "we would love to have a chat with you.",
        "Doc_type" : "email",
        "mobile_message" : "null"
    },
    {
        "message" : "Hi #name:, <br/> You're resume has been shortlisted for #jobProfile: <br/> Please reply to this mail for showing your interest. <br/> #hr_signature: <br/> #company: <br/> #date:",
        "message_key" : "shortlist_confirmation",
        "working" : True,
        "mobile_message" : "shortlist confirmation message #date:",
        "message_origin" : "RECRUIT",
        "message_subject" : "Shortlisted for #job_profile:",
        "version" : 1,
        "default" : True,
        "for" : "when candidate is shortlisted",
        "recruit_details" : "shortlist confirmation",
        "Doc_type" : "email"
    },
    {
        "Doc_type" : "email",
        "for" : "when candidate is rejected",
        "message" : "<p>Dear Applicant <br/> Thank you very much for taking the time to interview with us for the profile of #job_profile:. We regret to inform that you couldn't clear the subsequent rounds of the interview process but we do appreciate your interest in the company and the job.<br/>We wish you all the best for future endeavors <br/>Regards<br/> #hr_signature: </p>",
        "message_key" : "interviewee_reject",
        "message_origin" : "RECRUIT",
        "message_subject" : "interviewee Rejection",
        "recruit_details" : "Interviwee Reject",
        "version" : 1,
        "default" : True,
        "working" : True
    }
]
