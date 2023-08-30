from django.conf import settings
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.db.models.signals import post_save
from django.dispatch import receiver, Signal
from django.template.loader import render_to_string

from rest_framework import status 
from rest_framework.authtoken.models import Token
from rest_framework.response import Response


user_created = Signal()
welcome_email = Signal()
user_verify_email = Signal()
# user_login = Signal()
token_created = Signal()


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def generate_token(sender, instance, created, **kwargs):
    if created:
        token, created =Token.objects.get_or_create(user=instance)
        token_created.send(sender=instance.__class__, instance=instance, token=token)
        
        
user_created.connect(generate_token, sender=settings.AUTH_USER_MODEL)



# def login_user(sender, request, user, **kwargs):


# user_login.connect(login_user, sender=settings.AUTH_USER_MODEL)
# @receiver(user_created, sender=settings.AUTH_USER_MODEL)
# def send_welcome_mail(sender, instance, created, **kwargs):
#     if created:
#         subject = 'Welcome to Ikenga'
#         body = render_to_string(
#             'welcome.html',
#             {
#                 'user': instance,
#             }
#         )
#         email = EmailMessage(
#             subject= subject,
#             body=body,
#             from_email=settings.EMAIL_HOST_USER,
#             to=[instance.email]
#         )
#         email.content_subtype = 'html'
#         email.send()

# welcome_email.connect(send_welcome_mail, sender=settings.AUTH_USER_MODEL)

# request.auth.delete()
# request.session.flush()