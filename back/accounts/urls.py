from django.urls import path
from . import views
from rest_framework_jwt.views import obtain_jwt_token

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', obtain_jwt_token),
    path('mypageUser/<str:username>/', views.profile, name='profile'),
    path('confirm/', views.confirm, name='confirm'),
    path('confirm_num/', views.confirm_num, name='confirm_num'),
]
 