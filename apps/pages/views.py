from django.shortcuts import render
from django.contrib.auth.models import AnonymousUser  # for mock user fallback


def landing_page(request):
    return render(request, 'landing.html')


def login_page(request):
    return render(request, 'auth/login.html')


def register_user_page(request):
    return render(request, 'auth/register/register_user.html')


def register_doctor_page(request):
    return render(request, 'auth/register/register_doctor.html')


def farmer_dashboard(request):
    # Mock user data for now
    user = request.user if request.user.is_authenticated else AnonymousUser()
    user.first_name = "John"
    user.last_name = "Doe"
    user.email = "john@example.com"

    # Mock stats data
    stats = {
        "uploads": 12,
        "diseases": 5,
        "remedies": 4
    }

    # Mock recent detections
    recent_detections = [
        {"crop_name": "Cauliflower", "disease_name": "Black Rot", "date": "2025-07-24"},
        {"crop_name": "Cauliflower", "disease_name": "Downy Mildew", "date": "2025-07-22"},
    ]

    return render(request, 'dashboard/farmer/dashboard.html', {
        "user": user,
        "stats": stats,
        "recent_detections": recent_detections
    })


def farmer_profile(request):
    # Mock user data for now
    user = request.user if request.user.is_authenticated else AnonymousUser()
    user.first_name = "John"
    user.last_name = "Doe"
    user.email = "john@example.com"

    return render(request, 'dashboard/farmer/profile.html', {
        "user": user
    })

from django.shortcuts import render
from django.contrib.auth.models import AnonymousUser

def farmer_image_upload(request):
    user = request.user if request.user.is_authenticated else AnonymousUser()
    user.first_name = "John"

    result = {
        "crop_name": "Tomato",
        "disease_name": "Early Blight",
        "suggestions": [
            "Apply copper-based fungicide weekly.",
            "Ensure proper plant spacing for better airflow.",
            "Remove and destroy infected leaves immediately.",
            "Avoid overhead watering to minimize moisture on leaves.",
            "Use resistant crop varieties if available."
        ],
        "suggested_by": "Dr. Adeel Nazir (Plant Pathologist)"
    }

    return render(request, 'dashboard/farmer/image_upload.html', {
        "user": user,
        "result": result,
    })


def farmer_past_analyses(request):
    # Mock user data for now
    user = request.user if request.user.is_authenticated else AnonymousUser()
    user.first_name = "John"
    user.last_name = "Doe"
    user.email = "john@example.com"

    # Mock past analyses data
    past_analyses = [
        {"crop_name": "Cauliflower", "disease_name": "Black Rot", "date": "2025-07-24", "confidence": "95%"},
        {"crop_name": "Cauliflower", "disease_name": "Downy Mildew", "date": "2025-07-22", "confidence": "87%"},
        {"crop_name": "Cauliflower", "disease_name": "Healthy", "date": "2025-07-20", "confidence": "92%"},
    ]

    return render(request, 'dashboard/farmer/past_analyses.html', {
        "user": user,
        "past_analyses": past_analyses
    })
