from django.db import models
from django.db.models.fields import BooleanField, DateTimeField, IntegerField
# from django.db.models.base import Model
from django.conf import settings
from rest_framework.fields import CharField

# Create your models here.
class Recruit(models.Model):
    title = models.TextField()
    content = models.TextField()
    max_cnt = IntegerField()
    current_cnt = IntegerField(default=1)
    public_id = models.TextField()
    public_pw = models.TextField()
    ott_name = models.TextField(default='unknown')
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    user = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, null=True, related_name='otts')
    
    def __str__(self):
        return self.title

class Comment(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    recruit = models.ForeignKey(Recruit, on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return f'{self.content}'