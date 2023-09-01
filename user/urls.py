from django.urls import path
from .views import get_all_alumni, get_one_alumni_details, update_alumni, get_all_student, get_one_student_details, update_student

urlpatterns = [
    path('api/alumni/', get_all_alumni, name='all_alumni'),
    path('api/alumni/<int:alumni_id>/', get_one_alumni_details, name='alumni_details'),
    path('api/student/', get_all_student, name='all_students'),
    path('api/student/<int:student_id>/', get_one_student_details, name='student_details'),
    path('api/alumni/<int:alumni_id>/update', update_alumni, name='update_alumni'),
    path('api/student/<int:student_id>/update', update_student, name='update_student'),
]
