from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AnonymousUser


def landing_page(request):
    return render(request, 'landing.html')


def login_page(request):
    return render(request, 'auth/login.html')


def register_user_page(request):
    return render(request, 'auth/register/register_user.html')


def register_doctor_page(request):
    return render(request, 'auth/register/register_doctor.html')


def farmer_dashboard(request):
    # Use actual logged-in user, otherwise mock
    user = request.user if request.user.is_authenticated else AnonymousUser()

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
    user = request.user
    farmer_profile = getattr(user, "farmer_profile", None)
    return render(request, "dashboard/farmer/profile.html", {
        "user": user,
        "farmer_profile": farmer_profile,
    })



def farmer_image_upload(request):
    user = request.user if request.user.is_authenticated else AnonymousUser()

    result = {
        "crop_name": "Tomato",
        "disease_name": "Early Blight",
        "suggestions": [
            {"text": "Apply copper-based fungicide weekly.", "suggested_by": "Dr. Adeel Nazir"},
            {"text": "Ensure proper plant spacing for better airflow.", "suggested_by": "Dr. Sara Khan"},
            {"text": "Remove and destroy infected leaves immediately.", "suggested_by": "Dr. Ali Raza"},
            {"text": "Avoid overhead watering to minimize moisture on leaves.", "suggested_by": "Dr. Hina Ahmed"},
            {"text": "Use resistant crop varieties if available.", "suggested_by": "Dr. Adeel Nazir"},
        ]
    }

    return render(request, 'dashboard/farmer/image_upload.html', {
        "user": user,
        "result": result,
    })


def farmer_past_analyses(request):
    user = request.user if request.user.is_authenticated else AnonymousUser()

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
