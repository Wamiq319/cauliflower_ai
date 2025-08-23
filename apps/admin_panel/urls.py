from django.urls import path
from . import views

urlpatterns = [
    # Event management
    path('events/', views.manage_events, name='manage_events'),
    path('events/add/', views.add_event, name='add_event'),
    path('events/edit/<int:event_id>/', views.edit_event, name='edit_event'),
    path('events/delete/<int:event_id>/', views.delete_event, name='delete_event'),
    
    # Delete functionality
    path('delete/doctor/<int:doctor_id>/', views.delete_doctor, name='admin_panel_delete_doctor'),
    path('delete/farmer/<int:farmer_id>/', views.delete_farmer, name='admin_panel_delete_farmer'),
    
    # Update admin profile
    path('update-profile/', views.update_admin_profile, name='admin_panel_update_profile'),
]
