from django.urls import path
from .views import (
    landing_page,
    login_page,
    register_farmer_page,
    register_doctor_page,
)
from .farmer_views import (
    farmer_dashboard,
    farmer_profile,
    farmer_image_upload,
    farmer_open_case,
    farmer_past_analyses,
)
from .doctor_views import (
    doctor_dashboard,
    doctor_profile,
    doctor_suggest,
    doctor_past_suggestions,
    doctor_cases,
    doctor_case_details,
    doctor_solved_cases,
)
from .admin_views import (
    admin_dashboard,
    manage_farmers,
    manage_doctors,
    admin_profile,
)

urlpatterns = [
    # Landing and Auth Pages
    path('', landing_page, name='landing'),
    path('login/', login_page, name='login'),
    path('register/farmer/', register_farmer_page, name='register_farmer'),
    path('register/doctor/', register_doctor_page, name='register_doctor'),

    # Farmer Dashboard
    path('dashboard/farmer/', farmer_dashboard, name='farmer_dashboard'),
    path('dashboard/farmer/profile/', farmer_profile, name='farmer_profile'),
    path('dashboard/farmer/upload/', farmer_image_upload, name='farmer_image_upload'),
    path('dashboard/farmer/open-case/', farmer_open_case, name='farmer_open_case'),
    path('dashboard/farmer/analyses/', farmer_past_analyses, name='farmer_past_analyses'),

    # Doctor Dashboard
    path('dashboard/doctor/', doctor_dashboard, name='doctor_dashboard'),
    path('dashboard/doctor/profile/', doctor_profile, name='doctor_profile'),
    path('dashboard/doctor/suggest/', doctor_suggest, name='doctor_suggest'),
    path('dashboard/doctor/view_suggestions/', doctor_past_suggestions, name='doctor_past_suggestions'),
    path('dashboard/doctor/cases/', doctor_cases, name='doctor_cases'),
    path('dashboard/doctor/cases/<int:case_id>/', doctor_case_details, name='doctor_case_details'),
    path('dashboard/doctor/solved-cases/', doctor_solved_cases, name='doctor_solved_cases'),

    # Admin Dashboard
    path('dashboard/admin/', admin_dashboard, name='admin_dashboard'),
    path('dashboard/admin/farmers/', manage_farmers, name='manage_farmers'),
    path('dashboard/admin/doctors/', manage_doctors, name='manage_doctors'),
    path('dashboard/admin/profile/', admin_profile, name='admin_profile'),
]
