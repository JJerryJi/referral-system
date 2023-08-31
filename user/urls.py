from django.urls import path
from .views import get_all_alumni, get_one_alumni_details

urlpatterns = [
    path('api/alumni/', get_all_alumni, name='all_alumni'),
    path('api/alumni/<int:alumni_id>/', get_one_alumni_details, name='alumni_details'),
]
