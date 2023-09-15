from django.urls import path
from .views import JobView, Favorite_JobView, AlumniJobView
urlpatterns = [
    path('api/posts', JobView.as_view(), name='Alumni can post, modify, and delete job posts'),
    path('api/my_posts', AlumniJobView.as_view(), name='Alumni can view his job posts'),
    path('api/posts/<int:Job_post_id>', JobView.as_view(), name='Alumni can view job posts'),
    path('api/favorite_jobs', Favorite_JobView.as_view()),
    path('api/favorite_jobs/<int:favorite_job_id>', Favorite_JobView.as_view())

]