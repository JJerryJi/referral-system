from django.core.mail import send_mail
from celery import shared_task
from user.models import User
from django.conf import settings

@shared_task
def send_application_status_update_email(email: str):
    try:
        subject = 'Status update to the application'
        message = f'Here is the status update to your application. Please sign in to view details'
        recipient_list = [email]

        send_mail(subject=subject, message=message, from_email=settings.EMAIL_HOST_USER, recipient_list=recipient_list, fail_silently=False)
        return f'Successfully sent welcome email to {email}'
    except User.DoesNotExist:
        return f'User with email {email} not found'

    except Exception as e:
        return str(e)
