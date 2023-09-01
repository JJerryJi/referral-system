from django.urls import path
from .views import get_all_posts

urlpatterns = [
    path('api/job_posts/', get_all_posts, name='all_job_posts')
]