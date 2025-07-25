from django.urls import path
from .views import (
    landing_page,
    login_page,
    register_user_page,
    register_doctor_page,
    farmer_dashboard,
    farmer_profile,
    farmer_image_upload,
    farmer_past_analyses,
)

urlpatterns = [
    path('', landing_page, name='landing'),
    path('login/', login_page, name='login'),
    path('register/user/', register_user_page, name='register_user'),
    path('register/doctor/', register_doctor_page, name='register_doctor'),

    # Farmer Dashboard
    path('dashboard/farmer/', farmer_dashboard, name='farmer_dashboard'),
    path('dashboard/farmer/profile/', farmer_profile, name='farmer_profile'),
    path('dashboard/farmer/upload/', farmer_image_upload, name='farmer_image_upload'),
    path('dashboard/farmer/analyses/', farmer_past_analyses, name='farmer_past_analyses'),
]
