from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class User(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=245, null=False)
    firstname = models.CharField(max_length=200, null=True)
    lastname = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=150, null=True)
    age = models.PositiveIntegerField(null=True)
    password = models.CharField(max_length=100, null=False)

class Post(models.Model):
    title = models.CharField(max_length=200,null=False)
    content = models.CharField(max_length=350,null=False)
    creation_date =models.PositiveIntegerField(null=True)
    author=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
