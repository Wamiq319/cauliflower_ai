from django.urls import path
from .views import landing_page, login_page, register_user_page, register_doctor_page

urlpatterns = [
    path('', landing_page, name='landing'),
    path('login/', login_page, name='login'),
    path('register/user/', register_user_page, name='register_user'),
    path('register/doctor/', register_doctor_page, name='register_doctor'),
]
