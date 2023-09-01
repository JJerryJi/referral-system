from django.shortcuts import render
from django.http import JsonResponse, Http404
from .models import Job_post
# Create your views here.

def get_all_posts(request):
    all_posts = Job_post().get_all_post_info()
    response_data = {
        "success": True,
        "job_post": all_posts,
    }
    return JsonResponse(response_data)