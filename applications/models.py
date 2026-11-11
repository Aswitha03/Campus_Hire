from django.db import models
from django.contrib.auth.models import User
from jobs.models import Job
class Application(models.Model):
    STATUS=[("applied","Applied"),("shortlisted","Shortlisted"),("rejected","Rejected"),("selected","Selected")]
    student=models.ForeignKey(User,on_delete=models.CASCADE,related_name="applications")
    job=models.ForeignKey(Job,on_delete=models.CASCADE,related_name="applications")
    status=models.CharField(max_length=20,choices=STATUS,default="applied")
    applied_at=models.DateTimeField(auto_now_add=True)
    class Meta:
        constraints=[models.UniqueConstraint(fields=["student","job"],name="unique_student_job_application")]
