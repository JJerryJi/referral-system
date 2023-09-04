from django.urls import path
from .views import Student_ApplicationView

urlpatterns = [
    path('api/application/<int:application_id>', Student_ApplicationView.as_view(), name='Application'),
    path('api/application', Student_ApplicationView.as_view(), name='Application'),
]
