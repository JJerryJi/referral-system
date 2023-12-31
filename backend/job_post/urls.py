from django.urls import path
from .views import JobView, Favorite_JobView, AlumniJobView, LeaderBoardView
urlpatterns = [
    path('api/posts', JobView.as_view()),
    path('api/my_posts', AlumniJobView.as_view()),
    path('api/posts/<int:Job_post_id>', JobView.as_view()),
    path('api/favorite_jobs', Favorite_JobView.as_view()),
    path('api/favorite_jobs/<int:favorite_job_id>', Favorite_JobView.as_view()),
    path('api/leaderboard', LeaderBoardView.as_view()),

]