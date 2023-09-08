from django.urls import path
from .views import AlumniView, StudentView

urlpatterns = [
    path('api/alumni', AlumniView.as_view(), name='Only Superuser can view all Alumni''s profiles'),
    path('api/alumni/<int:alumni_id>', AlumniView.as_view(), name='Everyone can view a specific Alumni Profile; alumni can only modify&delete his/her own profile'),
    path('api/student', StudentView.as_view(), name='Only Superuser can view all Student''s profiles'),
    path('api/student/<int:student_id>', StudentView.as_view(), name='Everyone can view a specific Student Profile; student can only modify&delete his/her own profile'),
]
