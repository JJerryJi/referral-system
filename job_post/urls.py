from django.urls import path
from .views import JobView
urlpatterns = [
    path('api/posts', JobView.as_view(), name='all_job_posts'),
    path('api/posts/<int:Job_post_id>', JobView.as_view(), name='one_job_post')

]