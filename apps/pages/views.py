from django.shortcuts import render
from django.utils import timezone

# Model import for events
from apps.admin_panel.models import Event


# =============================================================================
# LANDING & AUTHENTICATION VIEWS
# =============================================================================

def landing_page(request):
    """Landing page."""
    return render(request, 'landing.html')


def login_page(request):
    """Login page."""
    return render(request, 'auth/login.html')


def register_farmer_page(request):
    """Farmer registration page."""
    return render(request, 'auth/register/register_farmer.html')


def register_doctor_page(request):
    """Doctor registration page."""
    return render(request, 'auth/register/register_doctor.html')


