from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Project(models.Model):
    title = models.CharField(max_length= 150)
    description = models.TextField()
    technology = models.CharField(max_length= 150)
    created_at = models.DateTimeField(auto_now_add= True)
    user = models.ForeignKey(User, on_delete= models.CASCADE)

    