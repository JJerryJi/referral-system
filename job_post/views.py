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
                    job_name = job_name, 
                    job_company  = job_company, 
                    job_requirement = job_requirement,
                    job_description = job_description,
                    question = question,
                )

            return JsonResponse({'success': True, 'message': 'New Job Post is created!', 'job_post': Job_post.get_one_post_by_id(new_job_post.id)})
        except Exception as e:
            return JsonResponse({'success':False, 'error': str(e)}, status = 500)
        

    def put(self, request, Job_post_id):
        try: 
            job_post = Job_post.objects.get(id=Job_post_id)
        except Job_post.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Job Post is not found. So the update fails!'}, status = 200)
        
        try: 
            data = json.loads(request.body)
            for key, value in data.items():
                if hasattr(data, key):
                    setattr(data, key, value)
            return JsonResponse({'success': True, 'message': f'Update Job Post #{job_post.id} success', 'job_post': Job_post.get_one_post_by_id(job_post.id)}, status = 200)
        except Exception as e: 
            return JsonResponse({'success':False, 'error': str(e)}, status = 500)
        
    
    def delete(self, request, Job_post_id):
        try: 
            job_post = Job_post.objects.get(id=Job_post_id)
            job_post.delete()
            return JsonResponse({'success': True, 'message': f"Successfully Delete Job Post # {Job_post_id}"}, status=200)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)