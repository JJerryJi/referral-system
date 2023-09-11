from django.shortcuts import render
from django.http import JsonResponse
from .models import Job_post, Favorite_job
from rest_framework.views import APIView
import json
from django.db import transaction
from user.models import Alumni, Student
from django.core.exceptions import PermissionDenied

# Create your views here.

class General_JobView(APIView):
    def get(self, request, Job_post_id=None):
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


class JobView(APIView):
    def get(self, request, Job_post_id=None):
        if Job_post_id == None:
            # superuser view
            if request.user.is_superuser:  
                job_lists = Job_post.get_all_post_info(admin_login=True)

            # alumni & student-view
            elif request.user.is_authenticated:
                all_posts = Job_post.objects.all()
                job_lists = []
                for post in all_posts:
                    cur_post = Job_post.get_one_post_by_id(post.id, admin_login= (request.user == post.alumni.user))
                    job_lists.append(cur_post)
            else:
                raise ValueError('You need to sign in to view job posts')
            
            response_data = {
                "success": True,
                "job_post": job_lists,
            }
            return JsonResponse(response_data, status = 200)
        # get a single post by id
        else:
            if request.user.is_superuser:
                post = Job_post.get_one_post_by_id(Job_post_id, admin_login=True)
            else:
                post = Job_post.get_one_post_by_id(Job_post_id)
            if post is None: return JsonResponse({"succes": False, 'error':'No job with such ID exist'}, status = 404)
            response_data = {
                "success": True,
                "job_post": post,
            }
            return JsonResponse(response_data, status = 200)
    
    def post(self, request):
        '''
        @request: 
        {
            "job_name": "String" (required),
            "job_company": "String" (required),
            "job_requirement": "String" (required),
            "job_description": "String" (required),
            "question": "String" (required)
        }
        '''

        try: 
            if request.user.is_authenticated:
                if request.user.role != 'alumni':
                    raise ValueError('Your user role is: Student or Superuser. You cannot create job posts') 
            else:
                raise ValueError('You cannot access the page if you are not authorized. Please log in.') 
            
            data = json.loads(request.body)

            
            # find the alumni from the requst.user
            alumnus = Alumni.objects.all()
            alumni = None
            for alm in alumnus:
                if alm.user == request.user:
                    alumni = alm

            job_name = data['job_name']
            job_company  = data['job_company'] 
            job_requirement = data['job_requirement']
            job_description = data['job_description']
            question = data['question']
            
            with transaction.atomic(): 
                Job_post.objects.create(
                    alumni = alumni, 
                    job_name = job_name, 
                    job_company  = job_company, 
                    job_requirement = job_requirement,
                    job_description = job_description,
                    question = question,
                )
            # use admin-login here just to return the updated job post 
            return JsonResponse({'success': True, 'message': 'New Job Post is created! You will be heard back from Team shortly'})
        except Exception as e:
            return JsonResponse({'success':False, 'error': str(e)}, status = 500)
        

    def put(self, request, Job_post_id):
        '''
        @request:
        for authenticated alumni: 
        {
            "job_name": "String" (optional),
            "job_company": "String" (optional),
            "job_requirement": "String" (optional),
            "job_description": "String" (optional),
            "job_open_status": "closed" (optional),
            ...
        }
        
        '''
        try:
            job_post = Job_post.objects.get(id=Job_post_id)
             
            if request.user.is_authenticated:
                if request.user != job_post.alumni.user and not request.user.is_superuser:
                    raise PermissionDenied('You are not authorized to make this change, because this is not your post!')
            else:
                raise PermissionDenied('You are not authorized to access this page. Please sign in.')
        
            data = json.loads(request.body)
            for key, value in data.items():
                if hasattr(job_post, key):
                    setattr(job_post, key, value)
                else:
                    raise ValueError(f'[{key}] in json does not exist in Job_post table. Update Fails')
            job_post.save()

            return JsonResponse({'success': True, 'message': f'Update Job Post #{job_post.id} is successful!', 'job_post': Job_post.get_one_post_by_id(job_post.id, admin_login=True)}, status=200)
        
        except Job_post.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Job Post is not found. So the update fails!'}, status = 404)
        except PermissionError as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=401)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)

        
    
    def delete(self, request, Job_post_id):
        try: 
            job_post = Job_post.objects.get(id=Job_post_id)
            if request.user.is_superuser: 
                pass
            elif request.user == job_post.alumni.user:
                pass 
            else:
                raise PermissionDenied('You are not authorized to delete this post, because it is not your post.')
            # delete this post in db 
            job_post.delete()
            return JsonResponse({'success': True, 'message': f"Successfully Delete Job Post # {Job_post_id}"}, status=200)
        except Job_post.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Job Post is not found. So the update fails!'}, status = 404)
        except PermissionError as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=401)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)


class Admin_JobView(APIView):
    # change the job_reviewing_status
    def put(self, request, Job_post_id):
        # TODO: Authorize the login as an admin 
        #... 
        ''' 
        @request: 
        {
            "job_reviewing_status": 'Pass/Fail'
        }
        '''
        try:
            job_post = Job_post.objects.get(Job_post_id)

            updated_status = request.data.get('job_reviewing_status')
            if updated_status not in ['Pass', 'Fail']:
                raise ValueError('The job_reviwing_status that you passed in is not in the possible list: "Pass" or "Fail"')
            
            # update the reivew_status & save
            job_post.job_review_status =  updated_status
            job_post.save()

        except Job_post.DoesNotExist:
            return JsonResponse({'success': False, 'error': f'This Job Post with #{Job_post_id} does not exist'}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)

    def get(self, request, Job_post_id=None):
        # TODO: Authorize the login as an admin 
        #... 

        if Job_post_id == None:
            all_posts = Job_post.get_all_post_info(admin_login=True)
            response_data = {
                "success": True,
                "job_post": all_posts,
            }
            return JsonResponse(response_data, status = 200)
        # get a single post by id
        else:
            post = Job_post.get_one_post_by_id(Job_post_id, admin_login=True)
            if post is None: return JsonResponse({"succes": False, 'error':'No job with such ID exist'}, status = 404)
            response_data = {
                "success": True,
                "job_post": post,
            }
            return JsonResponse(response_data, status = 200)
        
    def delete(self, request, Job_post_id):
        try: 
            Job_post.objects.get(id=Job_post_id).delete()
            return JsonResponse({'success':True, 'message': f'The deletion of the Job Post with ID #{Job_post_id} success!'})
        except Job_post.DoesNotExist:
            return JsonResponse({'success':False, 'error': f"This Job post with ID #{Job_post_id} does not exist"})
        except Exception as e:
            return JsonResponse({'success':False, 'error':str(e)})

class Favorite_JobView(APIView):
    def get(self, request, favorite_job_id=None):
        if favorite_job_id is None:
            try: 
                if not request.user.is_authenticated:
                    raise PermissionDenied('You are not view this page. please sign in first.')
                elif request.user.is_superuser:
                    response = {
                        'success': True,
                        'message': 'Here is all views of fav_table info (from superuser)', 
                        'favorite_jobs': Favorite_job.get_all_favorite_jobs()
                    }
                    return JsonResponse(response)
                elif request.user.role == 'student':
                    student = Student.objects.get(user=request.user)

                    response = {
                        'success': True,
                        'message': f'Here is the view of all fav_table info associated with the student # id {student.id}',
                        'favorite_jobs': []
                    }
                    for fav_job in Favorite_job.objects.all():
                        if fav_job.student_id == student.id:
                            response['favorite_jobs'].append(fav_job.get_one_favorite_job())
                    return JsonResponse(response)
                else:
                    raise PermissionDenied('Only superuser or student can view all information of favorite_job info')
            except Student.DoesNotExist as e:
                return JsonResponse({'success':False, "error": f"User with id # {request.user.id} does not exist"}, status=404)
            except PermissionDenied as e:
                return JsonResponse({'success':False, "error": str(e)}, status=401)
            except Exception as e:
                return JsonResponse({'success':False, "error": str(e)}, status=500)
        else:
            try: 
                fav_job = Favorite_job.objects.get(id = favorite_job_id)
                if request.user != Student.objects.get(id = fav_job.student_id).user and not request.user.is_superuser:
                    raise ValueError('You are not authorized to view this information, because it is not your favorite_job info.')
                response = {
                    'success': True, 
                    'message': 'one specific favorite_table info',
                    'favorite_jobs' : fav_job.get_one_favorite_job()
                }
                return JsonResponse(response)
            except Favorite_job.DoesNotExist:
                return JsonResponse({'success': False, 'error': f'The favorite_job with # {favorite_job_id} does not exist.'})
            except Exception as e: 
                return JsonResponse({'success':False, "error": str(e)})
        
    def delete(self, request, favorite_job_id):
        try:
            fav_job = Favorite_job.objects.get(id=favorite_job_id)
            if request.user != Student.object.get(id = fav_job.student_id).user and not request.user.is_superuser:
                raise PermissionDenied('You are not authorized to view this information, because it is your favorite_job info.')
            fav_job.delete()
            return JsonResponse({'success': True, 'error': f'The favorite_job with # {favorite_job_id} is deleted.'})
        except Favorite_job.DoesNotExist:
            return JsonResponse({"success": False, 'error': f'The favorite_job with ID {favorite_job_id} does not exist.'})
        except PermissionDenied as e:
            return JsonResponse({'success': False, 'error': str(e)})
        except Exception as e:
            return JsonResponse({"success": False, 'error': str(e)}) 
    
    def post(self, request):
        '''
        @request:
        {
        student_id: Integer, 
        job_id: Integer
        }
        '''
        try: 
            student_id = request.data.get('student_id')
            job_id = request.data.get('job_id')
            # make sure input is valid
            student = Student.objects.get(id = student_id)
            job = Job_post.objects.get(id = job_id)
            
            # authorization
            if request.user.is_anonymous:
                raise PermissionDenied("Please sign in as an authenaticated user.")
            elif request.user != student.user and not request.user.is_superuser:
                raise PermissionDenied('You are not authorized to add this fav_job info')
            
            # only one instance is allowed 
            if Favorite_job.objects.filter(student_id=student_id, job_id=job_id).first():
                raise PermissionDenied('You have already marked this job as saved! So you cannot save it again!')
            
            with transaction.atomic():
                Favorite_job.objects.create(
                    student_id = student_id, 
                    job_id = job_id
                )
            return JsonResponse({'success':False, 'message': "The new favorite_job is created!"})
        except Job_post.DoesNotExist:
            return JsonResponse({'success': False, 'error': f'The job post with # {job_id} does not exist.'})
        except Student.DoesNotExist:
            return JsonResponse({'success': False, 'error': f'The Student Profile  with # {student_id} does not exist.'})
        except PermissionDenied as e:
            return JsonResponse({'success': False, 'error': str(e)})
        except Exception as e: 
            return JsonResponse({"success": False, 'error': str(e)}) 