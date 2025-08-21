from django.urls import path
from . import views

urlpatterns = [
    # Delete functionality
    path('delete/doctor/<int:doctor_id>/', views.delete_doctor, name='admin_panel_delete_doctor'),
    path('delete/farmer/<int:farmer_id>/', views.delete_farmer, name='admin_panel_delete_farmer'),
    
    # Update admin profile
    path('update-profile/', views.update_admin_profile, name='admin_panel_update_profile'),
]
