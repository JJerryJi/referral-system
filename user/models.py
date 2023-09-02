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
    def get_all_alumni_info(cls, *args):
        all_alumni = cls.objects.all()
        alumni_list = []
        
        # for each alumni, call get_alumni_info_by_id
        for alumni in all_alumni:
            alumni_info = cls.get_alumni_info_by_id(alumni.id, *args)
            alumni_list.append(alumni_info)
        
        return alumni_list
    
    @classmethod
    def get_alumni_info_by_id(cls, alumni_id, *args):
        try: 
            alumni = cls.objects.get(id=alumni_id)
        except cls.DoesNotExist:
            return None 
        
        alumni_info = {
            "alumni_id": alumni.id,
        }
        user_table_info  = {}
        user_object = alumni.user
        
        for attribute in args:
            if hasattr(user_object, attribute):
                user_table_info[attribute] = getattr(user_object, attribute)

        alumni_info['user'] = user_table_info
        alumni_info['company_name'] = alumni.company_name
        alumni_info['modified_time'] = alumni.modified_time
        alumni_info['created_time'] = alumni.created_time
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

    @classmethod
    def get_all_student_info(cls, *args):
        students = cls.objects.all()
        student_list = []

        for student in students:
            student_info = cls.get_student_info_by_id(student.id, *args)
            student_list.append(student_info)
        
        return student_list
    

    @classmethod
    def get_student_info_by_id(cls, student_id, *args):
        try: 
            student = cls.objects.get(id = student_id)
        except cls.DoesNotExist:
            raise  
        student_info = {
                "user": {}, 
                "student.id" : student.id,
                "school": student.school,
                "year_in_school" : student.year_in_school, 
                "major" : student.major, 
                "graduation_year": student.graduation_year
            }
        user_info = {}
        for attribute in args:
            if hasattr(student.user, attribute): 
                user_info[attribute] = getattr(student.user, attribute)
        
        student_info['user'] = user_info
        return student_info 
    
