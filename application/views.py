import os, json
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
            # Get the uploaded PDF file data
            pdf_data = request.FILES.get('resume')

            if pdf_data is None:
                raise ValueError('you must upload your Resume')
            if pdf_data.name.split('.')[-1] != 'pdf':
                raise ValueError("you must submit an PDF version of your Resume")
            elif pdf_data.size > 5242880: # 5 megabytes
                raise ValueError("Your Resume size exceeds 5MB. Please upload a smaller one")
            
            # find student 
            try: 
                id = request.data.get('student_id')
                student_applicant = Student.objects.get(id=id)
            except Student.DoesNotExist:
                raise ValueError(f'Student who applied this job with id #{id} is not found. The student_id passed in is not correct. So this application fails.')
            

            # find job_post 
            try: 
                id = request.data.get('job_id')
                job_post = Job_post.objects.get(id=id)
            except Job_post.DoesNotExist:
                raise ValueError(f'Job post with this id #{id} is not found. The job_id passed in is not correct. So this application fails.')
            
            # Create an Application instance using the request data
            with transaction.atomic():
                application = Application.objects.create(
                    linkedIn=request.data.get('linkedIn'),
                    answer=request.data.get('answer'),
                    student=student_applicant, 
                    job = job_post
                )

            # Generate a unique filename for the resume PDF based on the application's ID
            resume_filename = f"{application.id}_resume.pdf"
            resume_path = os.path.join("/Users/jerry/Desktop/referral-system/application/resume", resume_filename)

            # Save the binary PDF data as a file
            with open(resume_path, 'wb') as resume_file:
                resume_file.write(pdf_data.read())

            # Update the 'resume_path' field in the Application instance
            application.resume_path = resume_path
            application.save()

            return JsonResponse({'success': True, 'message': 'Application created successfully.'}, status=201)
        
        except Exception as e:
            return JsonResponse({'success': True, "error": f"An error occurred: {str(e)}"}, status=500)

    # either admin view all application
    # or specific student view its application
    def get(self, request, application_id=None):
        # GET all applications
        if application_id is None:
            try:
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
                # Handle unexpected exceptions
                return JsonResponse({'success': False, 'error': str(e)}, status=500)

        # GET One application with ID provided
        # Content-type == applcation/json
            '''
            @request:
            student_id: Integer
            ''' 
        else:
            try:
                application = Application.objects.get(id=application_id)

                # Authorization for student: 
                try: 
                    if request.data.get('student_id') != application.student.id:
                        raise ValueError('You are not authorized to view this application, because it is not your application.')
                except: 
                    raise ValueError('You need to pass in ''student_id: interger'' in the request body for validation')
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


    #Only student can change its application
    def put(self, request, application_id):
        '''
        @request: 
        {
        'student_id' : Integer (required), 
        'resume': 'PDF.file' (optional),
        'linkedIn': 'url' (optional), 
        'answer' : "Char[]" (optional), 
        }
        '''
        try:
            application = Application.objects.get(id=application_id)

            # authorization & validation: 
            student_id = int(request.data.get('student_id'))
            if application.student.id != student_id:
                raise ValueError('Student is not authorized to change this application because it is not your application.')
            elif application.status != 'In Progress':
                raise ValueError('Student is not authorized to change this application because the decision is finalized')       
            elif application.application_date + timedelta(days=1) < datetime.now(pytz.timezone('UTC')):
                raise ValueError('Student is not authorized to change this application because the deadline for changing this application has expired.')
            
            # Iterate through the request data and update application attributes
            for key, value in request.data.items():
                if key == 'resume':
                    updated_pdf = request.FILES.get('resume')
                    if updated_pdf and updated_pdf.name.split('.')[-1] != 'pdf':
                        raise ValueError("You must submit a PDF version of your updated Resume")
                    elif updated_pdf and updated_pdf.size > 5242880:  # 5 megabytes
                        raise ValueError("Your updated Resume size exceeds 5MB. Please upload a smaller one")
                    
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
