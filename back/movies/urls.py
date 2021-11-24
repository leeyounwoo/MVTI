from django.urls import path
from . import views

app_name = 'movies'
urlpatterns = [
    path('', views.index, name='index'),
    path('detail/<int:movie_pk>', views.movie_detail),
    path('add_info/', views.add_info, name='add_info'),
    path('add_genre/', views.add_genre, name='add_genre'),
    path('ott_info/', views.ott_info, name='ott_info'),
    path('tournament', views.tournament),
    path('mypageMovie/<str:username>', views.mypageMovie),
    path('<int:movie_pk>/review/create/', views.review_create),
    path('<int:movie_pk>/review/delete/<int:review_pk>/', views.review_delete),

]
