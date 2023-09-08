from django.contrib import admin
from .models import Job_post, Favorite_job

# Register your models here.

@admin.register(Job_post)
class JobPostAdmin(admin.ModelAdmin):
    list_display = ('id', 'alumni', 'job_name', 'job_company', 'job_open_status', 'num_of_applicants', 'job_review_status')
    list_filter = ('job_open_status', 'job_review_status', 'num_of_applicants')
    search_fields = ('job_name', 'job_company', 'job_requirement')

@admin.register(Favorite_job)
class FavoriteJobAdmin(admin.ModelAdmin):
    list_display = ('id', 'student_id', 'job_id')
