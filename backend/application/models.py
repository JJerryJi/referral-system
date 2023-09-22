from django.db import models
from user.models import Student
from job_post.models import Job_post

class Application(models.Model):
    STATUS_CHOICES = [('In Progress', 'application in progress'), 
              ('Selected', 'application is selected'),
              ('Not-moving-forward', 'application is not selected')]
    id = models.AutoField(primary_key=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='In Progress')
    resume_path = models.CharField(max_length=200)
    linkedIn = models.URLField()
    application_date = models.DateTimeField(auto_now_add=True)
    answer =  models.TextField(max_length=2000)
    modified_date = models.DateTimeField(auto_now=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    job = models.ForeignKey(Job_post, on_delete=models.CASCADE)


    # get the student basic info 
    def get_student_applicant_info(self):
        student_info = Student.get_student_info_by_id(self.student.id) 
        if student_info is not None:
            return student_info
        else:
            raise ValueError(f'get this applicant with student id {self.student.id} info failed')

    # get the current application detail 
    def get_application_detail(self):
        response = {
                    "id": self.id, 
                    "status": self.status, 
                    "resume_path": self.resume_path,
                    "linkedIn": self.linkedIn,
                    "answer": self.answer, 
                    "application_date": self.application_date,
                    "modified_date": self.modified_date, 
                    "student_id" : self.student.id, 
                    "job_id" : self.job.id,
                    "job_name": self.job.job_name,
                    "user_id": self.student.user.id
                    }

        return response