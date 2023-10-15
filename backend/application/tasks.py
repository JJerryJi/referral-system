from django.core.mail import send_mail
from celery import shared_task
from user.models import User
from django.conf import settings

@shared_task
def send_application_status_update_email(email: str, application_id: int, job_company: str, username: str):
    try:
        subject = f'An Update from {job_company}'
        message = f'Dear {username}, ' \
                f'\n\tHere is the status update of your application (ID: {application_id}) at {job_company}. In order to view the details, please sign in to our Website. '\
                '\nBest, '\
                '\nReferral Finder Team.'
        recipient_list = [email]

        send_mail(subject=subject, message=message, from_email=settings.EMAIL_HOST_USER, recipient_list=recipient_list, fail_silently=False)
        return f'Sent Application STATUS update email to {email}'
    except User.DoesNotExist:
        return f'User with email {email} not found'

    except Exception as e:
        return str(e)
    
@shared_task
def send_submit_application_email(email: str, job_company: str, username: str):
    try:
        subject = f'Application to {job_company} successfully Submitted'
        message = f'Dear {username}, ' \
                f'\n\tYou have successfully submitted your application to Referral Post at {job_company}. The Alumni poster will soon examine your application. And we will update the status of your application as soon as possible. ' \
                '\n\tWish you all the best! ' \
                '\n\tReferral Finder Team'

        recipient_list = [email]

        send_mail(subject=subject, message=message, from_email=settings.EMAIL_HOST_USER, recipient_list=recipient_list, fail_silently=False)
        return f'Sent Submit Application email to {email}'
    except User.DoesNotExist:
        return f'User with email {email} not found'

    except Exception as e:
        return str(e)
    

@shared_task
def send_edit_application_email(email: str, job_company: str, username: str):
    try:
        subject = f'Application to {job_company} successfully Changed'
        message = f'Dear {username}, ' \
                f'\n\tYou have successfully modified your application to an role at {job_company}. The Alumni poster will soon examine your application. And we will update the status of your application as soon as possible. ' \
                '\n\tWish you all the best! ' \
                '\n\tReferral Finder Team'

        recipient_list = [email]

        send_mail(subject=subject, message=message, from_email=settings.EMAIL_HOST_USER, recipient_list=recipient_list, fail_silently=False)
        return f'Sent Edit Application email to {email}'
    except User.DoesNotExist:
        return f'User with email {email} not found'

    except Exception as e:
        return str(e)