# Standard Django imports
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AnonymousUser
from django.contrib import messages


# =============================================================================
# FARMER DASHBOARD VIEWS
# =============================================================================

@login_required
def farmer_dashboard(request):
    """Farmer dashboard with stats and recent detections."""
    # Use actual logged-in user
    user = request.user

    # Example stats (mock for now, replace with DB queries later)
    stats = {
        "uploads": 12,
        "diseases": 5,
        "remedies": 4
    }

    recent_detections = [
        {"crop_name": "Cauliflower", "disease_name": "Black Rot", "date": "2025-07-24"},
        {"crop_name": "Cauliflower", "disease_name": "Downy Mildew", "date": "2025-07-22"},
    ]

    return render(request, 'dashboard/farmer/dashboard.html', {
        "user": user,
        "stats": stats,
        "recent_detections": recent_detections
    })


@login_required
def farmer_profile(request):
    """Farmer profile page view."""
    user = request.user
    farmer_profile = getattr(user, "farmer_profile", None)
    return render(request, "dashboard/farmer/profile.html", {
        "user": user,
        "farmer_profile": farmer_profile,
    })


@login_required
def farmer_image_upload(request):
    """Image upload and analysis page for farmers."""
    user = request.user
    result = None
    uploaded_image = None
    
    if request.method == 'POST':
        # Handle file upload
        uploaded_file = request.FILES.get('plant_image')
        
        if uploaded_file:
            # Here you would integrate with your AI analysis backend
            # For now, using mock data - AI will detect crop type and disease
            
            # Mock AI analysis result (AI detects crop type automatically)
            result = {
                "crop_name": "Cauliflower",  # AI detected
                "disease_name": "Black Rot",  # AI detected
                "confidence": "92%",
                "uploaded_image": uploaded_file.name,
                "analysis_date": "2025-01-17",
                "analysis_id": "ANALYSIS_001",  # Unique ID for this analysis
                "suggestions": [
                    {
                        "title": "Immediate Treatment for Black Rot",
                        "disease_type": "black_rot",
                        "treatment": "Remove and destroy all infected plant parts immediately. Apply copper-based fungicide every 7-10 days. Ensure proper plant spacing for better air circulation.",
                        "prevention": "Use disease-resistant varieties. Avoid overhead watering. Maintain clean field practices. Rotate crops regularly.",
                        "best_practices": "Monitor plants regularly for early symptoms. Keep field free of plant debris. Use certified disease-free seeds.",
                        "priority": "high",
                        "suggested_by": "Dr. Adeel Nazir"
                    },
                    {
                        "title": "Cultural Control Methods",
                        "disease_type": "black_rot",
                        "treatment": "Implement strict sanitation practices. Remove all infected plant material and burn or bury it away from the field.",
                        "prevention": "Practice crop rotation with non-cruciferous crops for at least 3 years. Use raised beds for better drainage.",
                        "best_practices": "Avoid working in wet fields. Disinfect tools between uses. Maintain optimal soil pH (6.0-7.0).",
                        "priority": "medium",
                        "suggested_by": "Dr. Sara Khan"
                    }
                ]
            }
            
            uploaded_image = uploaded_file.name
            messages.success(request, f'Image analyzed successfully! Detected: {result["disease_name"]}')
        else:
            messages.error(request, 'Please select an image to upload.')

    return render(request, 'dashboard/farmer/image_upload.html', {
        "user": user,
        "result": result,
        "uploaded_image": uploaded_image
    })


@login_required
def farmer_open_case(request):
    """Farmer opens a case for doctor review."""
    if request.method == 'POST':
        analysis_id = request.POST.get('analysis_id')
        disease_name = request.POST.get('disease_name')
        crop_name = request.POST.get('crop_name')
        case_notes = request.POST.get('case_notes')
        
        # Here you would save the case to database
        # For now, just show success message
        
        messages.success(request, f'Case opened successfully! Doctors will review your {crop_name} case with {disease_name}.')
        return redirect('farmer_image_upload')
    
    return redirect('farmer_image_upload')


@login_required
def farmer_past_analyses(request):
    """Past analyses history for farmers."""
    user = request.user

    past_analyses = [
        {
            "crop_name": "Cauliflower",
            "disease_name": "Black Rot",
            "date": "2025-07-24",
            "confidence": "95%",
            "image_url": "https://via.placeholder.com/150",
            "suggestions": ["Remove infected leaves", "Apply copper fungicide", "Improve air circulation"]
        },
        {
            "crop_name": "Cauliflower",
            "disease_name": "Downy Mildew",
            "date": "2025-07-22",
            "confidence": "87%",
            "image_url": "https://via.placeholder.com/150",
            "suggestions": ["Use resistant varieties", "Ensure proper spacing", "Apply fungicide"]
        },
        {
            "crop_name": "Cauliflower",
            "disease_name": "Healthy",
            "date": "2025-07-20",
            "confidence": "92%",
            "image_url": "https://via.placeholder.com/150",
            "suggestions": ["Maintain routine care", "Monitor for pests", "Continue watering schedule"]
        },
    ]

    return render(request, 'dashboard/farmer/past_analyses.html', {
        "user": user,
        "past_analyses": past_analyses
    }) 