from django.http import JsonResponse, Http404
from django.shortcuts import get_object_or_404
from .models import Alumni, Student

def get_all_alumni(request):
    alumni_instance = Alumni()  # Create an instance of the Alumni model
    alumni_data = alumni_instance.get_all_alumni_info()  # Call the method to get alumni info
    
    response_data = {
        "success": True,
        "alumni": alumni_data,
    }
    
    return JsonResponse(response_data)

def get_one_alumni_details(request, alumni_id):
    alumni_info = Alumni().get_alumni_info_by_id(alumni_id)
    response_data = {
        "success": True,
        "alumni": alumni_info,
    }
    
    return JsonResponse(response_data)

def get_all_student(request):
    student_data = Student().get_all_student_info()
    response_data = {
        "success": True, 
        "student": student_data
    }    
    return JsonResponse(response_data)

def get_one_student_details(request, student_id):
    student_data = Student().get_student_info_by_id(student_id)
    response_data = {
        "success":True,
        "student": student_data
    }
    return JsonResponse(response_data)