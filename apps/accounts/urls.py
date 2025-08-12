from django.urls import path
from . import views

urlpatterns = [
    path('register/user/', views.register_user, name='register_user'),
    path('register/doctor/', views.register_doctor, name='register_doctor'),
     path('login/', views.user_login, name='login'),
]
