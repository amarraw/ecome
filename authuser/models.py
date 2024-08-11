from django.db import models

# Create your models here.

class ChangePass(models.Model):
    oldpass = models.CharField(max_length=50)
    newpass = models.CharField(max_length=50)
    compass = models.CharField(max_length=50)
