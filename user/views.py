from django.http import JsonResponse, Http404
from django.shortcuts import get_object_or_404
from .models import Alumni, Student
import json
from datetime import datetime
from django.views import View



def get_all_alumni(request):
    alumni_instance = Alumni()  # Create an instance of the Alumni model
    alumni_data = alumni_instance.get_all_alumni_info()  # Call the method to get alumni info
    
    response_data = {
        "success": True,
        "alumni": alumni_data,
    }
    
    return JsonResponse(response_data, status = 200)

def get_one_alumni_details(request, alumni_id):
    alumni_info = Alumni().get_alumni_info_by_id(alumni_id)
    if alumni_info is None:  return JsonResponse({"success": False, "error": "No Alumni data with such id is found"}, status = 404)
    response_data = {
        "success": True,
        "alumni": alumni_info,
    }
    
    return JsonResponse(response_data, status = 200)


def update_user_profile(user, profile_data):
    if 'first_name' in profile_data:
        user.first_name = profile_data['first_name']
    if 'last_name' in profile_data:
        user.last_name = profile_data['last_name']
    if 'email' in profile_data:
        user.email = profile_data['email']
    if 'location' in profile_data:
        user.location = profile_data['location']
    if 'password' in profile_data:
        user.password = profile_data['password']
    user.save()

def update_alumni(request, alumni_id):
        try:
            alumni = get_object_or_404(Alumni, id=alumni_id)
            content_type = request.content_type

            if content_type == 'application/json':
                data = json.loads(request.body)
            else:
                data = {}

            if 'user' in data:
                update_user_profile(alumni.user, data['user'])

            if 'company_name' in data:
                alumni.company_name = data['company_name']

            alumni.save()

            updated_alumni_info = {
                'alumni_id': alumni.id,
                'first_name': alumni.user.first_name,
                'last_name': alumni.user.last_name,
                'email': alumni.user.email,
                'location': alumni.user.location,
                'company_name': alumni.company_name
            }
            return JsonResponse({"success": True, "message": "Alumni updated successfully", "alumni": updated_alumni_info})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})


def get_all_student(request):
    student_data = Student.get_all_student_info()
    response_data = {
        "success": True, 
        "student": student_data
    }    
    return JsonResponse(response_data)

def get_one_student_details(request, student_id):
    student_data = Student.get_student_info_by_id(student_id)
    if student_data is None: return Http404("No Student data with such id is found")
    response_data = {
        "success":True,
        "student": student_data
    }
    return JsonResponse(response_data, status = 200)

def update_student(request, student_id):
    try:
            student = get_object_or_404(Student, id=student_id)
            content_type = request.content_type

            if content_type == 'application/json':
                data = json.loads(request.body)
            else:
                data = {}

            if 'user' in data:
                update_user_profile(student.user, data['user'])

            if 'major' in data:
                student.major = data['company_name']

            if 'school' in data:
                student.school = data['school']
            
            if 'year_in_school' in data:
                student.year_in_school = data['year_in_school']
            # save updated student profile in db
            student.modified_time = datetime.now()
            student.save()

            updated_student_info = {
                'student_id': student.id,
                'first_name': student.user.first_name,
                'last_name': student.user.last_name,
                'email': student.user.email,
                'location': student.user.location,
                'major': student.major,
                'school':student.school, 
                'year_in_school': student.year_in_school, 
                'modified_time' : student.modified_time
            }
            return JsonResponse({"success": True, "message": "Alumni updated successfully", "alumni": updated_student_info})
    except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})
