# Standard Django imports
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AnonymousUser


# =============================================================================
# LANDING & AUTHENTICATION VIEWS
# =============================================================================

def landing_page(request):
    """Landing page for the application."""
    return render(request, 'landing.html')


def login_page(request):
    """Login page view."""
    return render(request, 'auth/login.html')


def register_user_page(request):
    """User registration page view."""
    return render(request, 'auth/register/register_user.html')


def register_doctor_page(request):
    """Doctor registration page view."""
    return render(request, 'auth/register/register_doctor.html')

