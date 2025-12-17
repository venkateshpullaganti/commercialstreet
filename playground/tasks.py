import time
from templated_mail.mail import BaseEmailMessage
from celery import shared_task

from django.core.mail import send_mail
from templated_mail.mail import BaseEmailMessage

@shared_task
def notify_customers(args):
    # send multiple emails
    print(f"args received {args}")
    print("sending multiple emails")
    
    message = BaseEmailMessage(template_name="email/hello.html", context={"name":"Tanjiro"})
    message.send(["tanjiro_email_from_background_tasks@gmail.com"])


    send_mail("subject", "message", "commercialstreet@gmail.com", ["bob_email_bg_task@gmail.com"])

    time.sleep(10)

    print("sent multiple emails to user successfully")