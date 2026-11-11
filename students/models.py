from django.db import models
from django.contrib.auth.models import User
class StudentProfile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name="student_profile")
    roll_number=models.CharField(max_length=30,unique=True)
    department=models.CharField(max_length=80)
    cgpa=models.DecimalField(max_digits=4,decimal_places=2,default=0)
    backlogs=models.PositiveIntegerField(default=0)
    skills=models.TextField(blank=True)
    resume=models.FileField(upload_to="resumes/",blank=True,null=True)
    def __str__(self): return self.roll_number
