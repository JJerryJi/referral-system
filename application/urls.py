from django.urls import path
from .views import ApplicationView

urlpatterns = [
    path('api/application/<int:application_id>', ApplicationView.as_view(), name='Application'),
    path('api/application', ApplicationView.as_view(), name='Application'),

]
