from django.http import JsonResponse, Http404
from django.shortcuts import get_object_or_404
from .models import Alumni, Student
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
import json
from rest_framework.decorators import api_view



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

def get_all_student(request):
    student_data = Student().get_all_student_info()
    response_data = {
        "success": True, 
        "student": student_data
    }    
    return JsonResponse(response_data)

def get_one_student_details(request, student_id):
    student_data = Student().get_student_info_by_id(student_id)
    if student_data is None:  return JsonResponse({"success": False, "error": "No student data with such id is found"}, status = 404)
    response_data = {
        "success":True,
        "student": student_data
    }
    return JsonResponse(response_data, status = 200)


@api_view(['PUT'])
def update_alumni(request, alumni_id):
    if request.method == 'PUT':
        try:
            alumni = Alumni.objects.get(id=alumni_id)
        except Alumni.DoesNotExist:
            return JsonResponse({"success": False, "error": "Alumni not found"}, status=404)

        data = json.loads(request.body)

        if 'company_name' in data:
            alumni.company_name = data['company_name']

        # Add more fields here as needed

        alumni.save()

        response_data = {
            "success": True,
            "alumni": model_to_dict(alumni),
        }

        return JsonResponse(response_data)
    else:
        return JsonResponse({"success": False, "error": "Invalid method"}, status=405)