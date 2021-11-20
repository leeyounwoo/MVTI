from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db.models.fields import CharField


class Movie(models.Model):
    title = models.CharField(max_length=100)
    overview = models.TextField()
    released_date = models.DateField()
    poster_path = models.TextField()
    popularity = models.IntegerField()
    vote_average = models.IntegerField()
    vote_cnt = models.IntegerField()
