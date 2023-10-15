from django.core.mail import send_mail
from celery import shared_task
from user.models import User
from django.conf import settings
from django.core.mail import EmailMessage


@shared_task
def send_welcome_email(email: str):
    try:
        user = User.objects.filter(email=email).first()
        subject = 'Welcome to Referral Finder'
        content = f'Hello, {user.first_name}!\n\tWelcome to our website. Now you can sign in to your account and start explorating various referral opportunities! Wish you all the best finding your dream offer.\n Best,\nReferral Finder Team'
        recipient_list = [email]
        message = EmailMessage(
            subject,
            content,
            settings.EMAIL_HOST_USER,
            recipient_list,
        )
        message.attach_file(f'{settings.MEDIA_ROOT}/Logo.png', mimetype='application/octet-stream')
        message.send()
        # send_mail(subject=subject, message=message, from_email=settings.EMAIL_HOST_USER, recipient_list=recipient_list, fail_silently=False)
        return f'Successfully sent welcome email to {email}'
    except User.DoesNotExist:
        return f'User with email {email} not found'

    except Exception as e:
        return str(e)
