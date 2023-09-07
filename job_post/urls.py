from django.urls import path
from .views import General_JobView, JobView, Admin_JobView, Favorite_JobView
urlpatterns = [
    path('api/posts', JobView.as_view(), name='Alumni can post, modify, and delete job posts'),
    path('api/posts/<int:Job_post_id>', JobView.as_view(), name='Alumni can view job posts'),
    path('api/favorite_jobs', Favorite_JobView.as_view()),
    path('api/favorite_jobs/<int:favorite_job_id>', Favorite_JobView.as_view())

]