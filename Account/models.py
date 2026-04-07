from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class Baseuser(AbstractUser):
    address=models.CharField(max_length=100)
    phone=models.CharField(max_length=100)
    image=models.ImageField(upload_to="profile_pics",blank=True,null=True)  
    
    def __str__(self):
        return self.username

class Todolist(models.Model):
  title=models.CharField(max_length=100)
  description=models.TextField()
  created_at=models.DateTimeField(auto_now_add=True)
  updated_at=models.DateTimeField(auto_now=True)
  user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
  
  def __str__(self):
    return self.title 