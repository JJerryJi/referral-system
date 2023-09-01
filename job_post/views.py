from django.shortcuts import render
from django.http import JsonResponse
from .models import Job_post
from rest_framework.views import APIView
import json
from django.db import transaction
from user.models import Alumni
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
            if post is None: return JsonResponse({"succes": False, 'error':'No job with such ID exist'}, status = 404)
            response_data = {
                "success": True,
                "job_post": post,
            }
            return JsonResponse(response_data, status = 200)
    
    def post(self, request):
        try: 
            data = json.loads(request.body)
            try: 
                alumni = Alumni.objects.get(id=data['alumni_id'])
            except Alumni.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'Alumni not found'}, status=404)
        
            job_name = data['job_name']
            job_company  = data['job_company'] 
            job_requirement = data['job_requirement']
            job_description = data['job_description']
            question = data['question']
            
            with transaction.atomic(): 
                new_job_post = Job_post.objects.create(
                    alumni = alumni, 
                    job_name = data['job_name'], 
                    job_company  = data['job_company'], 
                    job_requirement = data['job_requirement'],
                    job_description = data['job_description'],
                    question = data['question'],
                )

            return JsonResponse({'success': True, 'message': 'New Job Post is created!', 'job_post': Job_post.get_one_post_by_id(new_job_post.id)})
        except Exception as e:
            return JsonResponse({'success':False, 'error': str(e)}, status = 500)