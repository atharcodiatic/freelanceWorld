from celery import shared_task 
from django.dispatch import receiver
from django.db.models.signals import  post_save
from .models import Contract
from smtplib import SMTPException
from django.conf import settings
from django.core.mail import send_mail
from .models import *


@shared_task
def send_email_by_celery(instance):
    print('mail by celery running')
    queryset = Contract.objects.filter(id=instance).first()
    email = queryset.proposal.user.email
    email_from = settings.EMAIL_HOST_USER
    job_title = queryset.proposal.job.title
    recipient_list = [email]
    subject = "Congratulations"
    message = f'We are delighted to inform you that you were hired for job :{job_title}'
    try:
        send_mail(subject, message, email_from, recipient_list)
    except SMTPException as e:
        print('There was an error sending an email. '+ e)
        return e
    return 'Mail sent'
    