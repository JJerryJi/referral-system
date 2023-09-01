from django.urls import path
from .views import get_all_posts, get_job_post_by_ID

urlpatterns = [
    path('api/posts/', get_all_posts, name='all_job_posts'),
    path('api/posts/<int:Job_post_id>/', get_job_post_by_ID, name='one_job_post')

]