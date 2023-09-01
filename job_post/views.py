from django.shortcuts import render
from django.http import JsonResponse, Http404
from .models import Job_post
# Create your views here.

def get_all_posts(request):
    all_posts = Job_post.get_all_post_info()
    response_data = {
        "success": True,
        "job_post": all_posts,
    }
    return JsonResponse(response_data)

def get_job_post_by_ID(request, Job_post_id):
    print(Job_post_id)
    post = Job_post.get_one_post_by_id(Job_post_id)
    if post is None: return Http404('No job with such ID exist')
    response_data = {
        "success": True,
        "job_post": post,
    }
    return JsonResponse(response_data)