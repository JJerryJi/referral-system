import os
import json
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Application
from user.models import Student
from job_post.models import Job_post
from django.db import transaction
from datetime import datetime, timedelta
import pytz
from django.core.exceptions import PermissionDenied


class Student_ApplicationView(APIView):
    def post(self, request):
        '''
        @request: 
        {
        'resume': 'PDF.file' (required),
        'student_id' : Integer (required), 
        'job_id': 'Integer' (required), 
        'linkedIn': 'url' (required), 
        'answer' : "Char[]" (required),

        }
        '''
        try:
            # TODO: need to authorize request.user is a student
            # ...
            
            # check valid student 
            try:
                id = request.data.get('student_id')
                student_applicant = Student.objects.get(id=id)
            except Student.DoesNotExist:
                raise ValueError(
                    f'Student who applied this job with id #{id} is not found. The student_id passed in is not correct. So this application fails.')

            # check valid job_post
            try:
                id = request.data.get('job_id')
                job_post = Job_post.objects.get(id=id)
                if job_post.job_open_status == 'closed': raise ValueError('This job has already closed. It no longer accepts any applications.')
                if job_post.job_review_status == 'In-review': raise ValueError('This job is still under review and not avaiable to the public. Please try again later when it is available.')
            except Job_post.DoesNotExist:
                raise ValueError(
                    f'Job post with this id #{id} is not found. The job_id passed in is not correct. So this application fails.')

            # avoid multiple applications: 
            if Application.objects.filter(student=student_applicant, job=job_post).first():
                raise ValueError('You have submitted this application. You cannot submit it more than once!')
            
            # Get the uploaded PDF file data
            pdf_data = request.FILES.get('resume')

            if pdf_data is None:
                raise ValueError('you must upload your Resume')
            if pdf_data.name.split('.')[-1] != 'pdf':
                raise ValueError(
                    "you must submit an PDF version of your Resume")
            elif pdf_data.size > 5242880:  # 5 megabytes
                raise ValueError(
                    "Your Resume size exceeds 5MB. Please upload a smaller one")
            
            # Create an Application instance using the request data
            with transaction.atomic():
                application = Application.objects.create(
                    linkedIn=request.data.get('linkedIn'),
                    answer=request.data.get('answer'),
                    student=student_applicant,
                    job=job_post
                )
                # add one to num_of_applicants
                job_post.num_of_applicants += 1
                job_post.save()
                print(job_post.num_of_applicants)

            # Generate a unique filename for the resume PDF based on the unique application's ID
            resume_filename = f"{application.id}_resume.pdf"
            resume_path = os.path.join(
                "/Users/jerry/Desktop/referral-system/application/resume", resume_filename)

            # Save the binary PDF data as a file
            with open(resume_path, 'wb') as resume_file:
                resume_file.write(pdf_data.read())

            # Update the 'resume_path' field in the Application instance
            application.resume_path = resume_path
            application.save()

            return JsonResponse({'success': True, 'message': 'Application created successfully.'}, status=201)

        except Exception as e:
            return JsonResponse({'success': True, "error": f"An error occurred: {str(e)}"}, status=500)

    def get(self, request, application_id):
        try:
            application = Application.objects.get(id=application_id)

            # Authorization for student:
            if request.user != application.student.user:
                raise ValueError('You are not authorized to view this application, because it is not your application. Please authorize yourself.')

            response = {
                'success': True,
                'message': f'Successful get this application with ID # {application.id}',
                'application': application.get_application_detail()
            }
            return JsonResponse(response, status=200)
        except Application.DoesNotExist:
            # Handle the case where the application is not found
            return JsonResponse({'success': False, 'error': f'Application with this ID #{application_id} does not exist.'}, status=404)
        except Exception as e:
            # Handle unexpected exceptions
            return JsonResponse({'success': False, 'error': str(e)}, status=500)

    # student change some info about their application
    def put(self, request, application_id):
        '''
        @request: 
        {
        'resume': 'PDF.file' (optional),
        'job_id': 'Integer' (optional), 
        'linkedIn': 'url' (optional), 
        'answer' : "Char[]" (optional), 
        }
        '''
        try:
            application = Application.objects.get(id=application_id)

            # TODO: Check if the user making the request is the owner of the application
            print(request.user)
            if application.student != request.user:
                raise ValueError(
                    'You are not authorized to change this application because it is not yours.')
            elif application.status != 'In Progress':
                raise ValueError(
                    'You are not authorized to change this application because the decision is finalized')
            elif application.application_date + timedelta(days=1) < datetime.now(pytz.timezone('UTC')):
                raise ValueError(
                    'You are not authorized to change this application because the deadline for changing this application has expired.')

            # Iterate through the request data and update application attributes
            for key, value in request.data.items():
                if key == 'resume':
                    updated_pdf = request.FILES.get('resume')
                    if updated_pdf and updated_pdf.name.split('.')[-1] != 'pdf':
                        raise ValueError(
                            "You must submit a PDF version of your updated Resume")
                    elif updated_pdf and updated_pdf.size > 5242880:  # 5 megabytes
                        raise ValueError(
                            "Your updated Resume size exceeds 5MB. Please upload a smaller one")

                    # Save the PDF data in the same path if provided
                    if updated_pdf:
                        with open(application.resume_path, 'wb') as resume_file:
                            resume_file.write(updated_pdf.read())
                elif hasattr(application, key):
                    setattr(application, key, value)

            # Save the changes
            application.save()

            # Return the updated application data
            response = {
                'success': True,
                'message': f'Successful update for application # {application.id}',
                'application': application.get_application_detail()
            }
            return JsonResponse(response, status=200)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})


class Alumni_ApplicationView(APIView):
    def get(self, request, application_id):
        '''
        @request:
        {
            "student_id": Integer
        }
        '''
        try:
            application = Application.objects.get(id=application_id)

            # TODO: Authorization: Check if the logged-in user is the alumni who posted the job
            # if request.user != application.job.alumni:
            #     raise PermissionDenied('You are not authorized to view this application because it is not your application.')

            response = {
                'success': True,
                'message': f'Successful get this application with ID # {application.id}. This alumni can see this application',
                'application': application.get_application_detail()
            }
            return JsonResponse(response, status=200)
        except Application.DoesNotExist:
            # Handle the case where the application is not found
            return JsonResponse({'success': False, 'error': f'Application with this ID #{application_id} does not exist.'}, status=404)
        except PermissionDenied as e:
            # Handle permission denied error
            return JsonResponse({'success': False, 'error': str(e)}, status=403)
        except Exception as e:
            # Handle unexpected exceptions
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    
    def put(self, request, application_id):
        '''
        @request:
        {
            "status": "Selected/Not-Moving-Forward"
        }
        '''
        try:
            application = Application.objects.get(id=application_id)

            # TODO: check if the logged-in user is the alumni who posted the job
            # if request.user != application.job.alumni:
            #     raise PermissionDenied('You are not authorized to change the status of this application because it is not your job posting.')

            # Get the new status from the request data
            new_status = request.data.get('status')

            # Validate the new status (you can add more validation logic here)
            if new_status not in ['Selected', 'Not-Moving-Forward']:
                raise ValueError('Invalid status value. Status must be "Selected" or "Not-Moving-Forward".')

            # Update the application status
            application.status = new_status
            application.save()

            response = {
                'success': True,
                'message': f'Successfully updated the status of application with ID #{application.id}',
                'application': application.get_application_detail()
            }
            return JsonResponse(response, status=200)

        except Application.DoesNotExist:
            return JsonResponse({'success': False, 'error': f'Application with this ID #{application_id} does not exist.'}, status=404)
        except PermissionDenied as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=403)
        except ValueError as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)



class Admin_ApplicationView(APIView):
    def get(self, request):
        try:
            # need to authentic the request.user == admin here
            # ... 
            application_list = []
            applications = Application.objects.all()
            for application in applications:
                application_list.append(application.get_application_detail())
            response = {
                'success': True,
                'message': 'Successful get all applications',
                'application': application_list
            }
            return JsonResponse(response, status=200)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
