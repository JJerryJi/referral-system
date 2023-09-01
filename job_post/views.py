from django.shortcuts import render
from django.http import JsonResponse
from .models import Job_post
from rest_framework.views import APIView
# Create your views here.

class JobView(APIView):
    def get(self, request, Job_post_id=None):
        # get all posts
        if Job_post_id == None:
            all_posts = Job_post.get_all_post_info()
            response_data = {
                "success": True,
                "job_post": all_posts,
            }
            return JsonResponse(response_data, status = 200)
        # get a single post by id
        else:
            post = Job_post.get_one_post_by_id(Job_post_id)
            if post is None: return JsonResponse({"succes": False, 'error':'No job with such ID exist'}, status = 200)
            response_data = {
                "success": True,
                "job_post": post,
            }
            return JsonResponse(response_data)