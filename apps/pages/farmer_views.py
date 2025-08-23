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
def farmer_image_upload(request):
    """Image upload and AI analysis for farmers."""
    user = request.user
    result = None
    uploaded_image = None

    if request.method == 'POST':
        uploaded_file = request.FILES.get('plant_image')

        if uploaded_file:
            # Mock AI analysis result
            result = {
                "crop_name": "Cauliflower",
                "disease_name": "Black Rot",
                "confidence": "92%",
                "uploaded_image": uploaded_file.name,
                "analysis_date": "2025-01-17",
                "analysis_id": "ANALYSIS_001",
                "suggestions": [
                    {
                        "title": "Immediate Treatment for Black Rot",
                        "disease_type": "black_rot",
                        "treatment": "Remove infected parts. Apply copper fungicide. Ensure air circulation.",
                        "prevention": "Use resistant varieties. Avoid overhead watering.",
                        "best_practices": "Monitor plants regularly. Keep field clean.",
                        "priority": "high",
                        "suggested_by": "Dr. Adeel Nazir"
                    },
                    {
                        "title": "Cultural Control Methods",
                        "disease_type": "black_rot",
                        "treatment": "Strict sanitation. Remove infected material.",
                        "prevention": "Crop rotation. Raised beds for drainage.",
                        "best_practices": "Disinfect tools. Maintain soil pH 6-7.",
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
    """Open a case for doctor review."""
    if request.method == 'POST':
        crop_name = request.POST.get('crop_name')
        disease_name = request.POST.get('disease_name')
        messages.success(request, f'Case opened! Doctors will review your {crop_name} case with {disease_name}.')
    return redirect('farmer_image_upload')


@login_required
def farmer_past_analyses(request):
    """Past analyses history."""
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