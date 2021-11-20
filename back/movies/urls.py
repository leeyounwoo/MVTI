from django.urls import path
from . import views

app_name = 'movies'
urlpatterns = [
    
    path('add_info/', views.add_info, name='add_info'),
]
