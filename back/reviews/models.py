from django.db import models
from django.db.models.fields import BooleanField, DateTimeField, IntegerField
# from django.db.models.base import Model
from django.conf import settings

class Review(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    review_movie = models.CharField(max_length=100)
    rank = models.IntegerField() 
    def __str__(self):
        return self.title

class ReviewComment(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    content = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.content}'
