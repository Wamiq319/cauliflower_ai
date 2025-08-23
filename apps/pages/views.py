from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

# Model imports
from apps.admin_panel.models import Event, Notification


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


# =============================================================================
# SHARED NOTIFICATION VIEW
# =============================================================================

@login_required
def mark_notification_read(request, notification_id):
    """
    Marks a single notification as read for the logged-in user.
    Works for both doctors and farmers.
    Returns a simple JSON message.
    """
    notification = get_object_or_404(Notification, id=notification_id, recipient=request.user)

    if not notification.is_read:
        notification.is_read = True
        notification.save()

    # Return JSON message
    return JsonResponse({
        "status": "success",
        "message": "Notification marked as read.",
        "notification_id": notification.id,
    })