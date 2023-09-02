from django.db import models
from user.models import Student
from job_post.models import Job_post

class Application(models.Model):
    STATUS_CHOICES = [('In Progress', 'application staus in progress'), 
              ('Selected', 'application is selected'),
              ('Not-moving-forward', 'application is not selected')]
    id = models.AutoField(primary_key=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='In Progress')
    resume_path = models.CharField(max_length=200)
    linkedIn = models.URLField()
    application_date = models.DateTimeField(auto_now_add=True)
    answer =  models.TextField(max_length=2000)
    modified_date = models.DateTimeField(auto_now=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    job = models.ForeignKey(Job_post, on_delete=models.CASCADE)
