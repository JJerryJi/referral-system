from django.core.mail import send_mail
from celery import shared_task
from user.models import User
from django.conf import settings
@shared_task
def send_welcome_email(email: str):
    try:
        user = User.objects.get(email=email)
        subject = 'Welcome to Referral_Finder'
        message = f'Hello, {user.first_name}! Welcome to our website.'
        recipient_list = [email]

        send_mail(subject=subject, message=message, from_email=settings.EMAIL_HOST_USER, recipient_list=recipient_list, fail_silently=False)
        return f'Successfully sent welcome email to {email}'
    except User.DoesNotExist:
        return f'User with email {email} not found'

    except Exception as e:
        return str(e)
