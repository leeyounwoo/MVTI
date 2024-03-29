from django.urls import path
from . import views


app_name = 'recruits'
urlpatterns = [
    path('', views.index),
    path('create/', views.create),
    path('<int:recruit_pk>/', views.detail),
    path('delete/<int:recruit_pk>/', views.delete),
    path('update/<int:recruit_pk>/', views.update),
    path('<int:recruit_pk>/comment/create/', views.comment_create),
    path('<int:recruit_pk>/comment/delete/<int:comment_pk>/', views.comment_delete),
    path('<int:recruit_pk>/pay/', views.pay, name='pay'),
    path('<int:recruit_pk>/pay/approval/', views.approval, name='approval'),
    path('mypageRecruit/<str:username>', views.mypageRecruit),
]
