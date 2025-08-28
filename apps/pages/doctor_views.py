# Standard Django imports
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.doctors.models import GeneralSuggestion
from apps.admin_panel.models import Event,Notification

from django.utils import timezone


# =============================================================================
# DOCTOR DASHBOARD VIEWS
# =============================================================================

@login_required
def doctor_dashboard(request):
    user = request.user
    is_approved = getattr(user.doctor_profile, 'is_approved', False) if hasattr(user, 'doctor_profile') else False
    
    total_suggestions = GeneralSuggestion.objects.filter(doctor=user).count()
    active_suggestions = total_suggestions
    total_cases_reviewed = 15

    # Upcoming events for the nearest date
    today = timezone.now().date()
    next_event = Event.objects.filter(date__gte=today).order_by('date').first()
    if next_event:
        upcoming_events = Event.objects.filter(date=next_event.date).order_by('created_at')
    else:
        upcoming_events = []

    return render(request, 'dashboard/doctor/dashboard.html', {
        "user": user,
        "stats": {
            "total_suggestions": total_suggestions,
            "active_suggestions": active_suggestions,
            "total_cases_reviewed": total_cases_reviewed,
        },
        "is_approved": is_approved,
        "upcoming_events": upcoming_events,
    })


@login_required
def doctor_profile(request):
    """Doctor profile page view."""
    user = request.user
    doctor_profile = getattr(user, "doctor_profile", None)
    return render(request, "dashboard/doctor/profile.html", {
        "user": user,
        "doctor_profile": doctor_profile,
    })


@login_required
def doctor_suggest(request):
    """Doctor suggestion page - redirects to create suggestion."""
    return redirect('doctor_create_suggestion')





# =============================================================================
# DOCTOR SUGGESTION VIEWS
# =============================================================================

@login_required
def doctor_past_suggestions(request):
    """List of past suggestions created by the logged-in doctor."""
    # Get all suggestions created by the current doctor
    past_suggestions = GeneralSuggestion.objects.filter(
        doctor=request.user
    ).order_by("-created_at")
    
    return render(request, 'dashboard/doctor/view_suggestions.html', {
        "past_suggestions": past_suggestions
    }) 

@login_required
def doctor_events(request):

    """Display events to doctors (read-only)."""
    events = Event.objects.all().order_by("-date")
    return render(request, "dashboard/doctor/doctor_events.html", {
        "user": request.user,
        "events": events,
    })


@login_required
@login_required
def doctor_notifications(request):
    """
    Display all notifications for the logged-in doctor.
    Unread notifications are highlighted.
    """
    notifications = request.user.notifications.all().order_by('-created_at')

    return render(request, "dashboard/doctor/doctor_notifications.html", {
        "notifications": notifications,
    })
