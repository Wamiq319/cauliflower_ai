import random
import os
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from django.conf import settings
from apps.doctors.models import GeneralSuggestion
from .models import Analysis, Case

def detect_disease_view(request):
    result = None
    if request.method == "POST" and request.FILES.get("plant_image"):
        image = request.FILES["plant_image"]

        # ---- Fake AI Logic (random disease choice) ----
        DISEASES = {
            "black_rot": "Black Rot",
            "downy_mildew": "Downy Mildew",
            "bacterial_spot": "Bacterial Spot Rot",
        }
        disease_key = random.choice(list(DISEASES.keys()))
        disease_name = DISEASES[disease_key]

        # ---- Fetch related suggestions ----
        suggestions_qs = GeneralSuggestion.objects.filter(
            disease_type=disease_key
        ).select_related("doctor")

        suggestions = []
        for s in suggestions_qs:
            doctor = s.doctor
            doctor_name = f"{doctor.first_name} {doctor.last_name}".strip()
            if not doctor_name:  # fallback to username if no first/last name
                doctor_name = doctor.username

            suggestions.append({
                "title": s.title,
                "treatment": s.treatment,
                "prevention": s.prevention,
                "best_practices": s.best_practices,
                "priority": s.priority,
                "suggested_by": doctor_name,
            })

        # ---- Build result object (without saving to database) ----
        result = {
            "crop_name": "Cauliflower",
            "disease_name": disease_name,
            "analysis_date": timezone.now().strftime("%Y-%m-%d %H:%M"),
            "suggestions": suggestions,
            "disease_key": disease_key,  # Store for case creation
        }

    return render(request, "dashboard/farmer/image_upload.html", {"result": result})

def open_case_view(request):
    if request.method == "POST":
        disease_name = request.POST.get("disease_name")
        crop_name = request.POST.get("crop_name")
        case_notes = request.POST.get("case_notes")
        disease_key = request.POST.get("disease_key")
        
        # Create analysis record when opening a case
        analysis = Analysis.objects.create(
            farmer=request.user,
            crop_name=crop_name,
            disease_name=disease_name,
        )
        
        # Create case
        case = Case.objects.create(
            farmer=request.user,
            analysis=analysis,
            title=f"Case for {crop_name} - {disease_name}",
            description=case_notes,
            priority='medium'
        )
        
        messages.success(request, f"Case #{case.id} opened successfully for {crop_name} with {disease_name}. A doctor will review your case soon.")
        
        return redirect("farmer_detect_disease")
    
    return redirect("farmer_detect_disease")
