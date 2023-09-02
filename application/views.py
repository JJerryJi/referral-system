import os
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Application
from user.models import Student
from job_post.models import Job_post

class ApplicationView(APIView):
    def post(self, request):
        try:
            # Get the uploaded PDF file data
            pdf_data = request.FILES.get('resume')
            if pdf_data.name.split('.')[-1] != 'pdf':
                raise ValueError("you must submit an PDF version of your Resume")
            elif pdf_data.size > 5242880: # 5 megabytes
                raise ValueError("Your Resume size exceeds 5MB. Please upload a smaller one")
            
            # find student 
            try: 
                id = request.data.get('student_id')
                student_applicant = Student.objects.get(id=id)
            except Student.DoesNotExist:
                raise ValueError(f'Student who applied this job with id #{id} is not found. The student_id passed in is not correct.')
            

            # find job_post 
            try: 
                id = request.data.get('job_id')
                job_post = Job_post.objects.get(id=id)
            except Job_post.DoesNotExist:
                raise ValueError(f'Job post with this id #{id} is not found. The job_id passed in is not correct.')
            
            # Create an Application instance using the request data
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

            return Response("Application created successfully.", status=status.HTTP_201_CREATED)
        
        except Exception as e:
            return Response({"error": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
