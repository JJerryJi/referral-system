from django.urls import path
from .views import General_JobView, Alumni_JobView, Admin_JobView
urlpatterns = [
    path('api/posts', General_JobView.as_view(), name='all after-reviewed job_posts available to everyone'),
    path('api/posts/<int:Job_post_id>', General_JobView.as_view(), name='a specific job after reivew by anyone'),
    path('api/alumni/posts', Alumni_JobView.as_view(), name='Alumni can post, modify, and delete job posts'),
    path('api/alumni/posts/<int:Job_post_id>', Alumni_JobView.as_view(), name='Alumni can view job posts'),
    path('api/admin/posts/<int:Job_post_id>', Admin_JobView.as_view(), name='Change the status review-status (and other fields) of a specific job post'),
    path('api/admin/posts', Admin_JobView.as_view(), name='Admin can view ALL job posts')

]