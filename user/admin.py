from django.contrib import admin
from .models import User, Alumni, Student

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'role', 'first_name', 'last_name', 'location', 'created_time', 'modified_time')
    list_filter = ('role',)
    search_fields = ('username', 'email', 'first_name', 'last_name')

@admin.register(Alumni)
class AlumniAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'company_name', 'created_time', 'modified_time')
    list_filter = ('created_time', 'modified_time')
    search_fields = ('user__username', 'company_name')

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'school', 'year_in_school', 'major', 'graduation_year','degree',)
    list_filter = ('year_in_school', 'graduation_year', 'created_time', 'modified_time')
    search_fields = ('user__username', 'school', 'major')
