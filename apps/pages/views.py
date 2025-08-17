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
    # Simulated user (for frontend display only)
    user = request.user if request.user.is_authenticated else AnonymousUser()
    user.first_name = "John"

    # Mock AI detection result (Python dictionary format)
    result = {
        "crop_name": "Tomato",
        "disease_name": "Early Blight",
        "suggestions": [
            {
                "text": "Apply copper-based fungicide weekly.",
                "suggested_by": "Dr. Adeel Nazir (Plant Pathologist)"
            },
            {
                "text": "Ensure proper plant spacing for better airflow.",
                "suggested_by": "Dr. Sara Khan (Horticulture Expert)"
            },
            {
                "text": "Remove and destroy infected leaves immediately.",
                "suggested_by": "Dr. Ali Raza (Agricultural Scientist)"
            },
            {
                "text": "Avoid overhead watering to minimize moisture on leaves.",
                "suggested_by": "Dr. Hina Ahmed (Plant Protection Specialist)"
            },
            {
                "text": "Use resistant crop varieties if available.",
                "suggested_by": "Dr. Adeel Nazir (Plant Pathologist)"
            }
        ]
    }

    return render(request, 'dashboard/farmer/image_upload.html', {
        "user": user,
        "result": result,
    })



def farmer_past_analyses(request):
    user = request.user if request.user.is_authenticated else AnonymousUser()
    user.first_name = "John"
    user.last_name = "Doe"
    user.email = "john@example.com"

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
        {
            "crop_name": "Cauliflower",
            "disease_name": "Aphid Infestation",
            "date": "2025-07-18",
            "confidence": "89%",
            "image_url": "https://via.placeholder.com/150",
            "suggestions": ["Spray neem oil", "Introduce ladybugs", "Remove infected parts"]
        },
        {
            "crop_name": "Cauliflower",
            "disease_name": "Clubroot",
            "date": "2025-07-16",
            "confidence": "91%",
            "image_url": "https://via.placeholder.com/150",
            "suggestions": ["Rotate crops", "Adjust soil pH", "Improve drainage"]
        },
        {
            "crop_name": "Cauliflower",
            "disease_name": "Leaf Spot",
            "date": "2025-07-14",
            "confidence": "86%",
            "image_url": "https://via.placeholder.com/150",
            "suggestions": ["Prune affected areas", "Use appropriate fungicide", "Clean tools regularly"]
        },
    ]

    return render(request, 'dashboard/farmer/past_analyses.html', {
        "user": user,
        "past_analyses": past_analyses
    })

    # Mock user data for now
    user = request.user if request.user.is_authenticated else AnonymousUser()
    user.first_name = "John"
    user.last_name = "Doe"
    user.email = "john@example.com"

    # Mock past analyses with images and suggestions
    past_analyses = [
        {
            "crop_name": "Cauliflower",
            "disease_name": "Black Rot",
            "date": "2025-07-24",
            "confidence": "95%",
            "suggestions": [
                "Remove infected leaves",
                "Apply copper-based bactericide",
                "Improve field drainage",
                "Avoid overhead watering",
                "Use disease-resistant varieties"
            ],
            "image_url": "https://via.placeholder.com/100?text=Cauliflower+1"
        },
        {
            "crop_name": "Cauliflower",
            "disease_name": "Downy Mildew",
            "date": "2025-07-22",
            "confidence": "87%",
            "suggestions": [
                "Use fungicides with metalaxyl",
                "Ensure good air circulation",
                "Rotate crops annually",
                "Avoid excess moisture",
                "Destroy infected plants"
            ],
            "image_url": "https://via.placeholder.com/100?text=Cauliflower+2"
        },
        {
            "crop_name": "Cauliflower",
            "disease_name": "Healthy",
            "date": "2025-07-20",
            "confidence": "92%",
            "suggestions": [
                "Maintain regular inspection",
                "Ensure balanced fertilization",
                "Keep consistent watering schedule",
                "Continue current practices",
                "Use organic pest control"
            ],
            "image_url": "https://via.placeholder.com/100?text=Cauliflower+3"
        },
    ]

    return render(request, 'dashboard/farmer/past_analyses.html', {
        "user": user,
        "past_analyses": past_analyses
    })