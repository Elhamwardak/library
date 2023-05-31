from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from django.contrib.auth.models import User
from .utils import send_email_task
from django.core.mail import send_mail
from django.conf import settings

def send_welcome_email(sender, instance, **kwargs): 
        send_email_task.delay('subject','message','elham.wardak.ew@gmail.com',['elham.wardak.ew@gmail.com'])

post_save.connect(send_welcome_email, sender=User)
