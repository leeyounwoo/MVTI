from django.contrib import admin
from .models import Review, Movie, Genre, Ott, Tournament

# Register your models here.
admin.site.register(Movie)
admin.site.register(Genre)
admin.site.register(Ott)
admin.site.register(Tournament)
admin.site.register(Review)
