import os
from celery import shared_task
from django.core.mail import send_mail
from dotenv import load_dotenv

load_dotenv()


@shared_task()
def register_message(message, email):
    mail_subject = 'Activation link has been sent to your email id'
    send_mail(mail_subject, message, os.environ.get('EMAIL_HOST_USER'),
              [email],
              fail_silently=False)
