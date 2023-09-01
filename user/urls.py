from django.urls import path
from .views import AlumniView, StudentView

urlpatterns = [
    path('api/alumni', AlumniView.as_view(), name='Alumni CRUD'),
    path('api/alumni/<int:alumni_id>', AlumniView.as_view(), name='Alumni CRUD'),
    path('api/student', StudentView.as_view(), name='all_students'),
    path('api/student/<int:student_id>', StudentView.as_view(), name='student_details'),
]
