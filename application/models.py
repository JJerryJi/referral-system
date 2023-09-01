from django.db import models

# Create your models here.

class Application(models.Model):
    STATUS_CHOICES = [('In Progress', 'application staus in progress'), 
              ('Selected', 'application is selected'),
              ('Not-moving-forward', 'application is not selected')]
    id = models.AutoField(primary_key=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    # resume = models.
    linkedIn = models.URLField()
    application_date = models.DateTimeField(auto_now_add=True)
    answer =  models.TextField(max_length=2000)
    modified_date = models.DateTimeField(auto_now=True)
