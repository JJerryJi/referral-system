from django.urls import path
from .views import Student_ApplicationView, Alumni_ApplicationView, Admin_ApplicationView

urlpatterns = [
    path('api/student/application/<int:application_id>', Student_ApplicationView.as_view(), name='Student view an Application'),
    path('api/student/application', Student_ApplicationView.as_view(), name='Student submit an Application'),
    path('api/admin/application', Admin_ApplicationView.as_view(), name='Admin view all Application'),
    path('api/alumni/application/<int:application_id>', Alumni_ApplicationView.as_view(), name='Alumni view Application'),

]
