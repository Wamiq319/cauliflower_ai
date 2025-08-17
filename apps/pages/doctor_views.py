# Standard Django imports
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages


# =============================================================================
# DOCTOR DASHBOARD VIEWS
# =============================================================================

@login_required
def doctor_dashboard(request):
    """Doctor dashboard with statistics."""
    user = request.user
    stats = {
        "total_suggestions": 8,
        "active_suggestions": 6,
        "total_cases_reviewed": 15
    }
    
    return render(request, 'dashboard/doctor/dashboard.html', {
        "user": user,
        "stats": stats
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
def doctor_case_suggestion(request, case_id):
    """Create suggestion for a specific case."""
    if request.method == 'POST':
        # Handle form submission for case suggestion
        treatment = request.POST.get('treatment', '')
        prevention = request.POST.get('prevention', '')
        notes = request.POST.get('notes', '')
        priority = request.POST.get('priority', '')
        
        # TODO: Save the suggestion to database
        # For now, just redirect with success message
        messages.success(request, 'Suggestion submitted successfully!')
        return redirect('doctor_dashboard')
    
    case = {
        "id": case_id,
        "farmer_name": "Ali Khan",
        "date": "2025-07-24",
        "status": "urgent",
        "disease_name": "Black Rot",
        "confidence": "92%",
        "image": {"url": "/static/image/Logo.png"}  # Mock image
    }
    return render(request, 'dashboard/doctor/case_suggestion.html', {
        "case": case
    })


@login_required
def doctor_submit_case_suggestion(request, case_id):
    """Submit case suggestion form."""
    if request.method == 'POST':
        # Handle form submission for case suggestion
        diagnosis_confirmation = request.POST.get('diagnosis_confirmation', '')
        custom_diagnosis = request.POST.get('custom_diagnosis', '')
        treatment = request.POST.get('treatment', '')
        prevention = request.POST.get('prevention', '')
        
        # TODO: Save the case suggestion to database
        # For now, just redirect with success message
        messages.success(request, 'Case recommendation submitted successfully!')
        return redirect('doctor_solved_cases')
    
    return redirect('doctor_case_details', case_id=case_id)


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
# DOCTOR SUGGESTION MANAGEMENT VIEWS
# =============================================================================

@login_required
def doctor_suggest(request):
    """Create general suggestion page."""
    if request.method == 'POST':
        # Handle form submission for general suggestion
        disease_type = request.POST.get('disease_type', '')
        title = request.POST.get('title', '')
        treatment = request.POST.get('treatment', '')
        prevention = request.POST.get('prevention', '')
        best_practices = request.POST.get('best_practices', '')
        priority = request.POST.get('priority', '')
        
        # TODO: Save the general suggestion to database
        # For now, just redirect with success message
        messages.success(request, 'Suggestion created successfully!')
        return redirect('doctor_past_suggestions')
    
    return render(request, 'dashboard/doctor/create_suggestion.html')


@login_required
def doctor_past_suggestions(request):
    """List of past suggestions created by doctor."""
    # Mock data for past suggestions
    past_suggestions = [
        {
            "id": 1,
            "disease": "Black Rot",
            "treatment": "Apply copper-based fungicide weekly",
            "prevention": "Ensure proper plant spacing",
            "created_at": "2025-07-20"
        },
        {
            "id": 2,
            "disease": "Downy Mildew",
            "treatment": "Use fungicides containing mancozeb",
            "prevention": "Avoid overhead watering",
            "created_at": "2025-07-18"
        }
    ]
    
    return render(request, 'dashboard/doctor/view_suggestions.html', {
        "past_suggestions": past_suggestions
    }) 