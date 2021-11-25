from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class User(AbstractUser):
    phone = models.CharField(max_length=15 ,blank=True)
    money = models.IntegerField(default=0)

class number(models.Model):
    num = models.IntegerField(default=0)