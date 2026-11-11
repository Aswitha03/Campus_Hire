from django.db import models
from django.contrib.auth.models import User
class Company(models.Model):
    recruiter=models.ForeignKey(User,on_delete=models.CASCADE,related_name="companies")
    name=models.CharField(max_length=150)
    description=models.TextField(blank=True)
    website=models.URLField(blank=True)
    def __str__(self): return self.name
