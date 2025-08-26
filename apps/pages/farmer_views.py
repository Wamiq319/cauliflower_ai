# Standard Django imports
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages


from apps.admin_panel.models import Event,Notification
from django.utils import timezone



# =============================================================================
# FARMER DASHBOARD VIEWS
# =============================================================================


@login_required
def farmer_dashboard(request):
    """Farmer dashboard with stats and recent detections."""
    user = request.user

    stats = {"uploads": 12, "diseases": 5, "remedies": 4}
    recent_detections = [
        {"crop_name": "Cauliflower", "disease_name": "Black Rot", "date": "2025-07-24"},
        {"crop_name": "Cauliflower", "disease_name": "Downy Mildew", "date": "2025-07-22"},
    ]

    # Get nearest upcoming events
    today = timezone.now().date()
    next_event = Event.objects.filter(date__gte=today).order_by('date').first()
    if next_event:
        upcoming_events = Event.objects.filter(date=next_event.date).order_by('created_at')
    else:
        upcoming_events = []

    return render(request, 'dashboard/farmer/dashboard.html', {
        "user": user,
        "stats": stats,
        "recent_detections": recent_detections,
        "upcoming_events": upcoming_events
    })


@login_required
def farmer_profile(request):
    """Farmer profile page."""
    user = request.user
    farmer_profile = getattr(user, "farmer_profile", None)
    return render(request, "dashboard/farmer/profile.html", {
        "user": user,
        "farmer_profile": farmer_profile,
    })



@login_required
def farmer_events(request):
    """Display events to farmers."""
    events = Event.objects.all().order_by("-date")
    return render(request, "dashboard/farmer/farmer_events.html", {
        "user": request.user,
        "events": events,
    })

def farmer_notifications(request):
    """
    Display all notifications for the logged-in farmer.
    Unread notifications are highlighted.
    """
    notifications = request.user.notifications.all().order_by('-created_at')

    return render(request, "dashboard/farmer/farmer_notifications.html", {
        "notifications": notifications,
    })