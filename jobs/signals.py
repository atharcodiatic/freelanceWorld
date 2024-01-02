from django.dispatch import receiver
from django.db.models.signals import  post_save
from .models import Contract
from smtplib import SMTPException
from django.conf import settings
from django.core.mail import send_mail
from .models import *
from .tasks import *

@receiver(post_save, sender=Contract)
def send_email_otp(sender, instance, created, **kwargs):
    print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
    task_result = send_email_by_celery.delay(instance.id)
    print(task_result.id)
    print('*********************************************')
    return True

    # print('signal running')
    # queryset = Contract.objects.filter(id=instance.id).first()
    # email = queryset.proposal.user.email
    # email_from = settings.EMAIL_HOST_USER
    # job_title = queryset.proposal.job.title
    # recipient_list = [email]
    
    # # # update the proposal 
    # # prop_obj = JobProposal.objects.get(id = queryset.proposal.user.id)
    # # prop_obj.status = 'ACCEPTED'
    # # prop_obj.save()
    # # # update job status 
    # # job = JobPost.objects.get(id=queryset.proposal.job.id)
    # # job.status = 'CLOSED'
    # # job.save()

    # subject = "Congratulations"
    # message = f'We are delighted to inform you that you were hired for job :{job_title}'
    # try:
    #     send_mail(subject, message, email_from, recipient_list)
    # except SMTPException as e:
    #     print('There was an error sending an email. '+ e)
    #     return