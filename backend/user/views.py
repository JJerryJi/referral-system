from django.http import JsonResponse, Http404
from django.shortcuts import get_object_or_404
from .models import Alumni, Student, User
import json
from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import transaction
from django.db.utils import IntegrityError
import traceback
from django.contrib.auth.hashers import make_password
from user.tasks import send_welcome_email

USER_ATTRIBUTES_TO_INCLUDE = ['id', 'first_name',
                              'last_name', 'email', 'username', 'location']

REGISTRATION_REQUIRED_FIELD = [
    'first_name', 'last_name', 'email', 'username', 'location', 'password']
ALUMNI_REQUIRED_FIELD = ['company_name']
STUDENT_REQUIRED_FIELD = ['password', 'major', 'degree', 'graduation_year']

# update user profile
# helper function


def update_user_profile(user, profile_data):
    for field in profile_data.keys():
        if hasattr(user, field):
            setattr(user, field, profile_data[field])
    user.modified_time = datetime.now()
    user.save()


class AlumniView(APIView):
    def get(self, request, alumni_id=None):
        try:
            if alumni_id is None:
                # only the authenticated superuser can view profile
                if not request.user.is_superuser:
                    raise ValueError(
                        'You cannot view this page, because you are not the superuser. Only the admin can all alumni profiles')
                alumni_data = Alumni.get_all_alumni_info(
                    *USER_ATTRIBUTES_TO_INCLUDE)

                response_data = {
                    "success": True,
                    "alumni": alumni_data,
                }
            else:
                alumni_info = Alumni.get_alumni_info_by_id(
                    alumni_id, *USER_ATTRIBUTES_TO_INCLUDE)
                if alumni_info is None:
                    return JsonResponse({"success": False, "error": "No Alumni data with such ID is found"}, status=404)

                response_data = {
                    "success": True,
                    "alumni": alumni_info,
                }

            return Response(response_data, status=200)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)

    def put(self, request, alumni_id):
        try:
            # only the authenticated user can view profile
            if request.user.is_anonymous:
                raise ValueError(
                    'You cannot view this page, because you do not log in.')
            # only the specific usr can make this change
            alumni = get_object_or_404(Alumni, id=alumni_id)
            if request.user.id != alumni.user.id:
                raise ValueError(
                    'You are not authorized to change this Alumni Profile, because this is not your account.')
            data = json.loads(request.body)
            update_user_profile(alumni.user, data)

            for key, value in data.items():
                if key == 'role':
                    raise PermissionError("You cannot change the role! ")
                if hasattr(alumni, key):
                    setattr(alumni, key, value)

            # change the modified time
            alumni.modified_time = datetime.now()
            alumni.save()

            return JsonResponse({
                "success": True,
                "message": "Alumni updated successfully",
                "alumni": Alumni.get_alumni_info_by_id(alumni_id, *USER_ATTRIBUTES_TO_INCLUDE),
            })
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})

    def post(self, request):
        '''
        @request: 
        {
            "first_name": 
            "last_name":
            "role": "alumni" (Has to match this) 
            "email"
            "username":
            "password":
            "location":
            "company_name":
        }
        '''
        try:
            data = json.loads(request.body)

            # Validate required fields
            required_fields = USER_ATTRIBUTES_TO_INCLUDE[1:] + ALUMNI_REQUIRED_FIELD
            extra_fields = set(required_fields).difference(data)
            if extra_fields:
                return JsonResponse({"success": False, "error": f"Missing required field"}, status=400)

            # Use a database transaction for atomicity
            with transaction.atomic():
                if data['role'] != 'alumni':
                    raise ValueError(
                        "Role must be 'alumni. So the creation of new alumni Failed'")

                # Create a new user instance
                new_user = User.objects.create(
                    last_name=data['last_name'],
                    first_name=data['first_name'],
                    email=data['email'],
                    username=data['username'],
                    password=make_password(data['password']),
                    location=data['location'],
                    role=data['role']
                )

                # Create a new alumni instance associated with the user
                new_alumni = Alumni.objects.create(
                    user=new_user,
                    company_name=data['company_name']
                )

                send_welcome_email.delay(data['email'])

            # return the information of the current alumni
            return JsonResponse(
                {
                    "success": True,
                    "message": "Alumni created successfully",
                    "alumni": Alumni.get_alumni_info_by_id(new_alumni.id, *USER_ATTRIBUTES_TO_INCLUDE)
                },
                status=201  # 201 Created status code
            )
        except IntegrityError as e:
            if  "username" in str(e): 
                return JsonResponse({"success": False, "error": "Username already exists. Please choose a different one."}, status=400)
            elif "email" in str(e): 
                return JsonResponse({"success": False, "error": "Email already exists. Please choose a different one."}, status=400)
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=500)

    def delete(self, request, alumni_id):
        try:
            alumni = Alumni.objects.get(id=alumni_id)
            # Authorization:
            if request.user.id != alumni.user.id:
                raise ValueError(
                    'You are not authorized to delete this profile, because it is not your profile')

            with transaction.atomic():
                alumni.user.delete()
                # Delete the alumni object
                alumni.delete()

            return JsonResponse({"success": True, "message": "Alumni deleted successfully"})
        except Alumni.DoesNotExist:
            return JsonResponse({'success': False, 'error': f'This alumni profile with ID {alumni_id} does not exist.'})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=500)


class StudentView(APIView):
    def get(self, request, student_id=None):
        try:
            # Only admin (superuser) has the power to view all profile
            if not student_id:
                if not request.user.is_superuser:
                    raise PermissionError(
                        'Only the superuser can view all student profile. Permission Denied')
                
                response_data = {
                    "success": True,
                    "student": Student.get_all_student_info(*USER_ATTRIBUTES_TO_INCLUDE, 'password')
                }
                return JsonResponse(response_data)
            else:
                try:
                    student = Student.objects.all().get(id=student_id)
                except Student.DoesNotExist:
                    raise ValueError(f'No Student data with such id ({student_id}) is found')
                student_data = student.get_student_info_by_id(*USER_ATTRIBUTES_TO_INCLUDE)
                response_data = {
                    "success": True,
                    "student": student_data
                }
                return JsonResponse(response_data, status=200)
        except ValueError as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=404)
        except PermissionError as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=401)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)

    def put(self, request, student_id):
        try:
            student = get_object_or_404(Student, id=student_id)
            # authorization
            if not request.user.is_superuser:
                if request.user.id != student.user.id:
                    raise ValueError(
                        'You cannot make change to this student profile, because it is not your profile.')

            data = json.loads(request.body)

            update_user_profile(student.user, data)

            # iterate over the request body
            for key, value in data.items():
                if key == 'role':
                    raise PermissionError("You cannot change the role! ")
                if hasattr(student, key):
                    setattr(student, key, value)

            # save updated student profile in db
            student.modified_time = datetime.now()
            student.save()

            return JsonResponse({"success": True, "message": "Student updated successfully", "student": student.get_student_info_by_id(*USER_ATTRIBUTES_TO_INCLUDE)}, status=200)
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=500)

    def post(self, request):
        '''
        @header:
        {
        Content-type: application/json
        }

        @request: 
        {
            "first_name": ""
            "last_name": ""
            "role": "student" (Has to match this) 
            "email": ""
            "username": ""
            "password": ""
            "location": "" 
            "school": ""
            "major": ""
            "degree": ""
            "graduation_year": ,
            "year_in_school": ,
        }
        '''
        try:
            data = json.loads(request.body)
            # Validate required fields
            required_fields = USER_ATTRIBUTES_TO_INCLUDE[1:] + STUDENT_REQUIRED_FIELD
            extra_fields = set(required_fields).difference(data)
            if extra_fields:
                return JsonResponse({"success": False, "error": f"Missing required field"}, status=400)
            
            with transaction.atomic():
                if data['role'] != 'student':
                    raise ValueError(
                        "Role must be student. Creation of new student Failed")

                # Create a new user instance
                new_user = User.objects.create(
                    last_name=data['last_name'],
                    first_name=data['first_name'],
                    email=data['email'],
                    username=data['username'],
                    password=make_password(data['password']),
                    location=data['location'],
                    role=data['role'],
                )

                # Create a new student instance associated with the user
                new_student = Student.objects.create(
                    user=new_user,
                    school=data['school'],
                    year_in_school=data['year_in_school'],
                    major=data['major'],
                    graduation_year=data['graduation_year'],
                    degree=data['degree'],
                )
                # send welcome email
                send_welcome_email.delay(data['email'])

            # return the information of the current alumni
            return JsonResponse(
                {
                    "success": True,
                    "message": "Student created successfully",
                    "student": new_student.get_student_info_by_id(*USER_ATTRIBUTES_TO_INCLUDE)
                },
                status=201  # 201 Created status code
            )
        except IntegrityError as e:
            if  "username" in str(e): 
                return JsonResponse({"success": False, "error": "Username already exists. Please choose a different one."}, status=400)
            elif "email" in str(e): 
                return JsonResponse({"success": False, "error": "Email already exists. Please choose a different one."}, status=400)
        except Exception as e:
            traceback.print_exc()
            return JsonResponse({"success": False, "error": f'{str(e)}.\n It is either because the username or the email is taken. Please try again'}, status=500)

    def delete(self, request, student_id):
        try:
            student = get_object_or_404(Student, id=student_id)
            if request.user.is_anonymous:
                raise ValueError(
                    'You cannot view this page, because you do not log in.')
            if request.user.id != student.user.id:
                raise ValueError(
                    'You cannot delete this student profile, because it is not your account. Please log in.')
            student.user.delete()
            # Delete the student object
            student.delete()

            return JsonResponse({"success": True, "message": "Student deleted successfully"})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=500)

# test 
def send_welcome_email_view(request):
    if request.method == 'GET':
        try:
            # Replace 'user@example.com' with the email address to which you want to send the welcome email.
            email_to_send = 'jerryji040506@g.ucla.edu'
            
            # Trigger the Celery task to send the welcome email asynchronously.
            send_welcome_email.delay(email_to_send)

            return JsonResponse({'success': True, 'message': f'Welcome email will be sent to {email_to_send}.'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    else:
        # Handle other HTTP methods (e.g., POST, PUT, DELETE) if needed.
        return JsonResponse({'success': False, 'error': 'Only GET requests are allowed for this view.'})