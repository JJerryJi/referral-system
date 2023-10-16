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
        job_lists = [post.get_one_post(admin_login=admin_login) for post in all_posts]
        return job_lists
    
    def get_one_post(self, permission=False):
        if not permission:
            if self.job_review_status == 'In-review':
                return {"job_id": self.id, 'job_review_status':'In-review'}

        post_info = {
            'job_id' : self.id, 
            'alumni_id' : self.alumni.id,
            'job_name': self.job_name,
            'job_company' : self.job_company,
            'job_requirement' : self.job_requirement, 
            'job_description' : self.job_description,
            'job_open_status' : self.job_open_status,
            'job_question' : self.question, 
            'num_of_applicants' : self.num_of_applicants, 
            'job_review_status' : self.job_review_status,
            'job_created_time' : self.created_time
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
