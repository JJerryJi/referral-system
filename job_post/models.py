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
    def get_all_post_info(self):
        all_posts = Job_post.objects.all()
        job_lists = []

        for post in all_posts:
            post_info = {
                'job_id' : post.id, 
                'alumni_id' : post.alumni.id,
                'job_name': post.job_name,
                'job_company' : post.job_company,
                'job_requirement' : post.job_requirement, 
                'job_description' : post.job_description,
                'job_open_status' : post.job_open_status,
                'job_question' : post.question, 
                'num_of_applicants' : post.num_of_applicants, 
                'job_review_status' : post.job_review_status,
            }
            job_lists.append(post_info)
        return job_lists