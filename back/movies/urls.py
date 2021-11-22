from django.urls import path
from . import views

app_name = 'movies'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:movie_pk>/', views.detail, name='detail'),
    path('add_info/', views.add_info, name='add_info'),
    path('add_genre/', views.add_genre, name='add_genre'),
    path('ott_info/', views.ott_info, name='ott_info'),
]
