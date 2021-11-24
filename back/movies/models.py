from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db.models.fields import CharField


class Genre(models.Model):
    genre_id = models.IntegerField()
    genre_name = models.CharField(max_length=10)

class Ott(models.Model):
    name = models.CharField(max_length=20)
    image = models.TextField(null=True)

class Movie(models.Model):
    idx = models.IntegerField()
    title = models.CharField(max_length=100)
    eng_title = models.CharField(max_length=100)
    overview = models.TextField()
    released_date = models.DateField()
    poster_path = models.TextField()
    popularity = models.IntegerField()
    vote_average = models.IntegerField()
    vote_cnt = models.IntegerField()

    movie_genre = models.ManyToManyField(
        Genre,
        related_name='movie_genre',
        blank=True,
        null=True,
    )
    movie_ott = models.ManyToManyField(
        Ott,
        related_name='movie_ott',
        blank=True,
        null=True,
    )

class Review(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    rating = models.IntegerField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='movie_comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
class Tournament(models.Model) :
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tournaments')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)