from django.db import models
from user.models import Alumni
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
    job_requirement = models.TextField(max_length=255)
    job_description = models.TextField(max_length=255)
    job_open_status = models.CharField(max_length=10, choices=OPENING_STATUS, default = 'acccept')
    question = models.TextField(max_length=255)
    num_of_applicants = models.IntegerField(default=0)
    job_review_status = models.CharField(max_length=10, choices=REVIEWING_STATUS,  default='In-review')
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)

    @classmethod
    def get_all_post_info(cls):
        all_posts = cls.objects.all()
        job_lists = []

        for post in all_posts:
            job_lists.append(cls.get_one_post_by_id(post.id))
        return job_lists
    
    @classmethod
    def get_one_post_by_id(cls, job_id):
        try: 
            job_post = cls.objects.get(id=job_id)
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
        }

        return post_info