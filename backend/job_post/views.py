from django.shortcuts import render
from django.http import JsonResponse
from .models import Job_post, Favorite_job
from rest_framework.views import APIView
import json
from django.db import transaction
from application.models import Application
from user.models import Alumni, Student
from django.core.exceptions import PermissionDenied
import traceback

# Create your views here.
class JobView(APIView):
    def get(self, request, Job_post_id=None):
        print(request.headers)
        print(dir(request))
        if Job_post_id == None:
            # superuser view
            if request.user.is_superuser:  
                job_lists = Job_post.get_all_post_info(admin_login=True)

            # alumni & student-view
            elif request.user.is_authenticated:
                all_posts = Job_post.objects.all().order_by('-created_time')
                job_lists = []
                for post in all_posts:
                    cur_post = Job_post.get_one_post_by_id(post.id, admin_login=(request.user == post.alumni.user))
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
            elif request.user.role == 'alumni':
                has_student_applied_before = True
                post = Job_post.get_one_post_by_id(Job_post_id)
            elif request.user.role == 'student':
                has_student_applied_before = False
                # find student object: 
                post = Job_post.get_one_post_by_id(Job_post_id)
                for student in Student.objects.all():
                    if student.user == request.user: 
                        this_student = student
                # check if this requested user has already submitted an application before:
                if Application.objects.filter(student=this_student, job=Job_post.objects.get(id=Job_post_id)).first():
                    has_student_applied_before = True
                
            if post is None: return JsonResponse({"succes": False, 'error':'No job with such ID exist'}, status = 404)
            response_data = {
                "success": True,
                "has_student_applied_before": has_student_applied_before,
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
                    raise ValueError('Your role is student. So not authorized to create job posts') 
            else:
                raise ValueError('You cannot access the page if you are not authorized. Please log in.') 
            
            data = json.loads(request.body)

            
            # find the alumni from the requst.user
            alumnus = Alumni.objects.all()
            alumni = None
            for alm in alumnus:
                if alm.user == request.user:
                    alumni = alm
            if not alumni:
                return JsonResponse({'success': False, "message": "You are not authorized to create new job post."}, status=403) 
            
            job_name = data['job_name']
            job_company  = data['job_company'] 
            job_requirement = data['job_requirement']
            job_description = data['job_description']
            question = data['job_question']
            
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
            return JsonResponse({'success': True, 'message': 'New Job Post is created! You will be heard back from Team shortly'}, status=201)
        except Exception as e:
            traceback.print_exc()
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
            print(data)
            for key, value in data.items():
                if hasattr(job_post, key):
                    setattr(job_post, key, value)
                elif key == 'job_question':
                    setattr(job_post, 'question', value)
                elif key == 'alumni_id' or key == 'job_id':
                    continue
                else:
                    raise ValueError(f'[{key}] in json does not exist in Job_post table. Update Fails')
            job_post.save()

            return JsonResponse({'success': True, 'message': f'Update Job Post #{job_post.id} is successful!', 'job_post': Job_post.get_one_post_by_id(job_post.id, admin_login=True)}, status=200)
        
        except Job_post.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Job Post is not found. So the update fails!'}, status = 404)
        except PermissionDenied as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=403)
        except Exception as e:
            traceback.print_exc()
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
            with transaction.atomic():
                job_post.delete()
            return JsonResponse({'success': True, 'message': f"Successfully Delete Job Post # {Job_post_id}"}, status=200)
        except Job_post.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Job Post is not found. So the update fails!'}, status = 404)
        except PermissionError as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=401)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)

class AlumniJobView(APIView):
    def get(self, request):
        try: 
            if request.user.is_authenticated:
                if request.user.role == 'alumni':
                    # find that request alumni
                    alumni = Alumni.objects.all().get(user = request.user)
                    my_posts = Job_post.objects.all().order_by('-created_time').filter(alumni=alumni)
                    job_lists = []
                    for post in my_posts:
                        cur_post = Job_post.get_one_post_by_id(post.id, admin_login=True)
                        job_lists.append(cur_post)
                else:
                    raise PermissionDenied('Role: Student are not allowed to view this page.')
            else:
                raise ValueError('You need to sign in to view job posts')
            
            response_data = {
                "success": True,
                "job_post": job_lists,
            }
            return JsonResponse(response_data, status = 200)
        except PermissionDenied as e: 
            return JsonResponse({"success":False, "error":str(e)}, status=403)
        except Exception as e:
            return JsonResponse({"success":False, "error": str(e)}, status=500)


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
                    print('stu', student)
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
                traceback.print_exc()
                return JsonResponse({'success':False, "error": str(e)}, status=500)
        else:
            try: 
                fav_job = Favorite_job.objects.get(id = favorite_job_id)
                if request.user != Student.objects.get(id = fav_job.student_id).user and not request.user.is_superuser:
                    raise PermissionDenied('You are not authorized to view this information, because it is not your favorite_job info.')
                response = {
                    'success': True, 
                    'message': 'one specific favorite_table info',
                    'favorite_jobs' : fav_job.get_one_favorite_job()
                }
                return JsonResponse(response)
            except Favorite_job.DoesNotExist:
                return JsonResponse({'success': False, 'error': f'The favorite_job with # {favorite_job_id} does not exist.'}, status=404)
            except PermissionDenied as e:
                return JsonResponse({'success':False, "error": str(e)}, status=401)
            except Exception as e: 
                return JsonResponse({'success':False, "error": str(e)}, status=500)
        
    def delete(self, request, favorite_job_id):
        try:
            fav_job = Favorite_job.objects.get(id=favorite_job_id)
            print(fav_job)
            print(request.user)
            print(Student.objects.get(id = fav_job.student_id).user)
            if request.user.is_superuser:
                pass 
            elif request.user != Student.objects.get(id = fav_job.student_id).user:
                raise PermissionDenied('You are not authorized to view this information, because it is not your favorite_job info.')
            fav_job.delete()
            return JsonResponse({'success': True, 'message': f'The favorite_job with # {favorite_job_id} is just deleted.'}, status=200)
        except Favorite_job.DoesNotExist:
            return JsonResponse({"success": True, 'message': f'The favorite_job with ID {favorite_job_id} has already been deleted.'}, status=200)
        except PermissionDenied as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=403)
        except Exception as e:
            return JsonResponse({"success": False, 'error': str(e)}, status=500) 
    
    def post(self, request):
        '''
        @request:
        {
        job_id: Integer
        }
        '''
        try: 
            # authorization
            if request.user.is_anonymous:
                raise PermissionDenied("Please sign in as an authenaticated user.")
            
            student = Student.objects.get(user = request.user)

            job_id = request.data.get('job_id')
            # make sure input is valid
            job = Job_post.objects.get(id = job_id)
        
            
            # only one instance is allowed 
            if Favorite_job.objects.filter(student_id=student.id, job_id=job_id).first():
                raise ValueError('You have already marked this job as saved! So you cannot save it again!')
            
            with transaction.atomic():
                Favorite_job.objects.create(
                    student_id = student.id, 
                    job_id = job_id
                )
            return JsonResponse({'success':True, 'message': "The new favorite_job is created!"}, status=200)
        except Job_post.DoesNotExist:
            return JsonResponse({'success': False, 'error': f'The job post with # {job_id} does not exist.'}, status=404)
        except Student.DoesNotExist:
            return JsonResponse({'success': False, 'error': f'The Student Profile  with # {student.id} does not exist.'}, status=404)
        except PermissionDenied as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=403)
        except Exception as e: 
            return JsonResponse({"success": False, 'error': str(e)}, status=500) 