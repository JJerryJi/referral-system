from django.db import models
from user.models import Alumni, Student
# Create your models here.

class Job_post(models.Model):
    OPENING_STATUS = [
        ('accept', 'Accept'),
        ('closed', 'Closed'),
    ]

    REVIEWING_STATUS = [
        ('In-review', 'Under-review'),
        ('Pass', 'Able to display'),
        ('Fail', 'Not pass the check')
    ]
    id = models.AutoField(primary_key=True)
    alumni = models.ForeignKey(Alumni, on_delete=models.CASCADE)
    job_name = models.CharField(max_length=128)
    job_company = models.CharField(max_length=64)
    job_requirement = models.TextField(max_length=2000)
    job_description = models.TextField(max_length=2000)
    job_open_status = models.CharField(max_length=10, choices=OPENING_STATUS, default = 'accept')
    question = models.TextField(max_length=255)
    num_of_applicants = models.IntegerField(default=0)
    job_review_status = models.CharField(max_length=10, choices=REVIEWING_STATUS,  default='In-review')
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return str(self.job_name) + ' at ' + str(self.job_company)
    @classmethod
    def get_all_post_info(cls, admin_login=False):
        all_posts = cls.objects.all()
        job_lists = []

        for post in all_posts:
            cur_post = cls.get_one_post_by_id(post.id, admin_login=admin_login) 
            job_lists.append(cur_post)
        return job_lists
    
    @classmethod
    def get_one_post_by_id(cls, job_id, admin_login=False):
        try: 
            job_post = cls.objects.get(id=job_id)
            # if the job_post is not being reviewed, only return limited info
            if not admin_login:
                if job_post.job_review_status == 'In-review':
                    return {"job_id": job_post.id, 'job_review_status':'In-review'}
        except Job_post.DoesNotExist:
            return None 
        post_info = {
            'job_id' : job_post.id, 
            'alumni_id' : job_post.alumni.id,
            'job_name': job_post.job_name,
            'job_company' : job_post.job_company,
            'job_requirement' : job_post.job_requirement, 
            'job_description' : job_post.job_description,
            'job_open_status' : job_post.job_open_status,
            'job_question' : job_post.question, 
            'num_of_applicants' : job_post.num_of_applicants, 
            'job_review_status' : job_post.job_review_status,
            'job_created_time' : job_post.created_time
        }
        
        return post_info
    
class Favorite_job(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.IntegerField()
    job_id = models.IntegerField()

    def get_one_favorite_job(self):
        current_job_post = Job_post.objects.all().get(id=self.job_id)
        response = {
            "id" : self.id, 
            "student_id" : self.student_id, 
            "job_id" : self.job_id, 
            "job_open_status": True if current_job_post.job_open_status == 'accept' else False,
        }
        return response
    
    @classmethod
    def get_all_favorite_jobs(self):
        all_fav_jobs = Favorite_job.objects.all()
        list_fav_jobs = []
        for fav_job in all_fav_jobs:
            list_fav_jobs.append(fav_job.get_one_favorite_job())
        return list_fav_jobs
