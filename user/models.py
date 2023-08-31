from django.db import models

# Create your models here.

from django.db import models

class User(models.Model):
    ROLES = [
        ('student', 'Student'),
        ('alumni', 'Alumni'),
    ]
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=32)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=32)
    role = models.CharField(max_length=10, choices=ROLES)
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    location = models.CharField(max_length=255)
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username


class Alumni(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=255)
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.company_name}"
    
    @classmethod
    def get_all_alumni_info(self):
        all_alumni = Alumni.objects.all()
        alumni_list = []
        
        for alumni in all_alumni:
            alumni_info = {
                "alumni_id": alumni.id,
                "first_name": alumni.user.first_name,
                "last_name": alumni.user.last_name,
                "email": alumni.user.email,
                "company_name": alumni.company_name,
            }
            alumni_list.append(alumni_info)
        
        return alumni_list
    
    @classmethod
    def get_alumni_info_by_id(self, alumni_id):
        alumni = Alumni.objects.get(id=alumni_id)
        alumni_info = {
                "alumni_id": alumni.id,
                "first_name": alumni.user.first_name,
                "last_name": alumni.user.last_name,
                "email": alumni.user.email,
                "company_name": alumni.company_name,
        }
        return alumni_info

class Student(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    school = models.CharField(max_length=32)
    year_in_school = models.PositiveIntegerField()
    major = models.CharField(max_length=32)
    graduation_year = models.DateTimeField()
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.school}"

