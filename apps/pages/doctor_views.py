# Standard Django imports
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.doctors.models import GeneralSuggestion


# =============================================================================
# DOCTOR DASHBOARD VIEWS
# =============================================================================

@login_required
def doctor_dashboard(request):
    """Doctor dashboard with statistics."""
    user = request.user
    
    # Check if doctor is approved
    is_approved = getattr(user.doctor_profile, 'is_approved', False) if hasattr(user, 'doctor_profile') else False
    
    # Get real statistics from the database
    total_suggestions = GeneralSuggestion.objects.filter(doctor=user).count()
    active_suggestions = GeneralSuggestion.objects.filter(doctor=user).count()  # For now, all suggestions are considered active
    total_cases_reviewed = 15  # This would come from a Case model when you have one
    
    stats = {
        "total_suggestions": total_suggestions,
        "active_suggestions": active_suggestions,
        "total_cases_reviewed": total_cases_reviewed
    }
    
    return render(request, 'dashboard/doctor/dashboard.html', {
        "user": user,
        "stats": stats,
        "is_approved": is_approved
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
# DOCTOR CASE MANAGEMENT VIEWS
# =============================================================================

@login_required
def doctor_cases(request):
    """List of pending cases for doctors."""
    # Mock data for pending cases
    cases = [
        {"id": 1, "farmer_name": "Ali Khan", "disease_name": "Black Rot", "date": "2025-07-24", "status": "urgent", "confidence": "92%"},
        {"id": 2, "farmer_name": "Sara Ahmed", "disease_name": "Downy Mildew", "date": "2025-07-23", "status": "normal", "confidence": "87%"},
        {"id": 3, "farmer_name": "Raza Shah", "disease_name": "Bacterial Spot", "date": "2025-07-22", "status": "normal", "confidence": "78%"},
    ]
    return render(request, 'dashboard/doctor/cases.html', {
        "cases": cases
    })


@login_required
def doctor_case_details(request, case_id):
    """Detailed view of a specific case."""
    case = {
        "id": case_id,
        "farmer_name": "Ali Khan",
        "date": "2025-07-24",
        "status": "urgent",
        "disease_name": "Black Rot",
        "confidence": "92%",
        "image": {"url": "/static/image/Logo.png"}  # Mock image
    }
    return render(request, 'dashboard/doctor/case_details.html', {
        "case": case
    })


@login_required
def doctor_solved_cases(request):
    """List of solved cases."""
    # Mock data for solved cases
    solved_cases = [
        {
            "id": 1,
            "farmer_name": "Ali Khan",
            "original_disease": "Black Rot",
            "doctor_diagnosis": "Confirmed: Black Rot",
            "treatment": "Apply copper-based fungicide weekly for 3 weeks",
            "prevention": "Ensure proper plant spacing and avoid overhead watering",
            "solved_date": "2025-07-20"
        },
        {
            "id": 2,
            "farmer_name": "Sara Ahmed",
            "original_disease": "Downy Mildew",
            "doctor_diagnosis": "Confirmed: Downy Mildew",
            "treatment": "Use fungicides containing mancozeb every 7 days",
            "prevention": "Improve air circulation and avoid overhead watering",
            "solved_date": "2025-07-18"
        }
    ]
    return render(request, 'dashboard/doctor/solved_cases.html', {
        "solved_cases": solved_cases
    })


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