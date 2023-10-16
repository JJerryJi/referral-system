from django.db import models
from django.core.exceptions import ValidationError
# Create your models here.

from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLES = [
        ('student', 'Student'),
        ('alumni', 'Alumni'),
        ('admin', 'Admin')
    ]
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50, null=False, blank=False)
    last_name = models.CharField(max_length=30, null=False, blank=False)
    email = models.EmailField(unique=True, null=False, blank=False) 
    role = models.CharField(max_length=10, choices=ROLES, null=False, blank=False)
    location = models.CharField(max_length=255, null=False, blank=False)
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        # Ensure that the role value is one of the predefined choices
        if self.role not in dict(self.ROLES).keys():
            raise ValidationError('Validation Error: the input value for role is not in the list of [''student'', ''alumni'', ''admin'']')
        super().save()

class Alumni(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False, blank=False)
    company_name = models.CharField(max_length=255, null=False, blank=False)
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user.username)
    
    @classmethod
    def get_all_alumni_info(cls, *args):
        all_alumni = cls.objects.all()
        alumni_list = []
        
        # for each alumni, call get_alumni_info_by_id
        for alumni in all_alumni:
            alumni_info = alumni.get_alumni_info_by_id(*args)
            alumni_list.append(alumni_info)
            
        return alumni_list
    
    def get_alumni_info_by_id(self, *args):
        alumni_info = {
            "alumni_id": self.id,
        }
        user_table_info  = {}
        for attribute in args:
            if hasattr(self.user, attribute):
                user_table_info[attribute] = getattr(self.user, attribute)

        alumni_info['user'] = user_table_info
        alumni_info['company_name'] = self.company_name
        alumni_info['modified_time'] = self.modified_time
        alumni_info['created_time'] = self.created_time
        return alumni_info

    class Meta:
        verbose_name_plural = 'Alumni'
        
class Student(models.Model):
    DEGREES = [
        ('BS', 'Bacholor of Science'),
        ('MS', 'Master of Science')
    ]
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    school = models.CharField(max_length=32, null=False, blank=False)
    year_in_school = models.PositiveIntegerField()
    major = models.CharField(max_length=32, null=False, blank=False)
    degree = models.CharField(max_length=3, choices=DEGREES)
    graduation_year = models.DateTimeField()
    created_time = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    modified_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.school}"

    @classmethod
    def get_all_student_info(cls, *args):
        students = cls.objects.all()
        student_list = [student.get_one_student_info(*args) for student in students]
        return student_list
    

    def get_one_student_info(self, *args):
        student_info = {
                "user": {}, 
                "student_id" : self.id,
                "school": self.school,
                "year_in_school" : self.year_in_school, 
                "major" : self.major, 
                "degree": 'Bacholor of Science' if self.degree == 'BS' else 'Master of Science', # render the value
                "graduation_year": self.graduation_year
            }
        user_info = {}
        for attribute in args:
            if hasattr(self.user, attribute): 
                user_info[attribute] = getattr(self.user, attribute)
        
        student_info['user'] = user_info
        return student_info 
    
