from django.contrib import admin
from .models import Application

# Register your Application model here.

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'job', 'status', 'application_date', 'answer', 'linkedIn', 'resume_path', 'modified_date')
    list_filter = ('status', 'application_date')
    search_fields = ('student__user__username','student__user__first_name', 'student__user__last_name', 'job__job_name', 'job__job_company')

    def get_student_full_name(self, obj):
        return f"{obj.student.first_name} {obj.student.last_name}"
    get_student_full_name.short_description = 'Student'

    def get_job_name(self, obj):
        return obj.job.job_name
    get_job_name.short_description = 'Job'

    def get_student_email(self, obj):
        return obj.student.email
    get_student_email.short_description = 'Student Email'
