from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Case, Analysis, CaseMessage
import random
from apps.doctors.models import GeneralSuggestion  # Ensure this import is correct
from django import forms


# =============================================================================
# CASE MESSAGE FORM
# =============================================================================
class CaseMessageForm(forms.ModelForm):
    class Meta:
        model = CaseMessage
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Type your message...'})
        }

# =============================================================================
# FARMER CASE LIST VIEW
# =============================================================================
@login_required
def farmer_cases_list(request):
    cases = Case.objects.filter(farmer=request.user).select_related('analysis').order_by('-created_at')
    return render(request, 'dashboard/farmer/cases_list.html', {
        'cases': cases,
        'cases_count': cases.count()
    })

# =============================================================================
# FARMER CASE DETAIL VIEW
# =============================================================================
@login_required
def farmer_case_detail(request, case_id):
    case = get_object_or_404(
        Case.objects.select_related('analysis').prefetch_related('messages'),
        id=case_id, 
        farmer=request.user
    )
    messages_qs = case.messages.all()
    
    if request.method == 'POST':
        form = CaseMessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.case = case
            message.sender = request.user
            message.save()
            messages.success(request, "Message sent successfully!")
            return redirect('farmer_case_detail', case_id=case.id)
    else:
        form = CaseMessageForm()
    
    return render(request, 'dashboard/farmer/case_detail.html', {
        'case': case,
        'messages': messages_qs,
        'form': form
    })

# =============================================================================
# DISEASE DETECTION VIEW
# =============================================================================
@login_required
def detect_disease_view(request):
    result = None
    doctor_list = []
    
    if request.method == "POST" and request.FILES.get("plant_image"):
        image = request.FILES["plant_image"]

        # Fake AI Logic (random disease choice)
        DISEASES = {
            "black_rot": "Black Rot",
            "downy_mildew": "Downy Mildew",
            "bacterial_spot_rot": "Bacterial Spot Rot",
        }
        disease_key = random.choice(list(DISEASES.keys()))
        disease_name = DISEASES[disease_key]

        # Fetch doctor suggestions
        suggestions_qs = GeneralSuggestion.objects.filter(disease_type=disease_key).select_related("doctor")
        suggestions = []
        for s in suggestions_qs:
            doctor = s.doctor
            doctor_name = f"{doctor.first_name} {doctor.last_name}".strip() or doctor.username
            doctor_list.append({
                "id": doctor.id,
                "name": doctor_name,
                "email": doctor.email
            })
            suggestions.append({
                "title": s.title,
                "treatment": s.treatment,
                "prevention": s.prevention,
                "best_practices": s.best_practices,
            })

        # Build result object with global disease info
        result = {
            "crop_name": "Cauliflower",
            "disease_name": disease_name,
            "analysis_date": timezone.now().strftime("%Y-%m-%d %H:%M"),
            "suggestions": suggestions,
            "disease_key": disease_key,
            "general_info": DISEASE_GLOBAL_DATA.get(disease_key, {})
        }

    return render(request, "dashboard/farmer/image_upload.html", {
        "result": result,
        "doctor_list": doctor_list
    })

# =============================================================================
# OPEN CASE VIEW
# =============================================================================
@login_required
def open_case_view(request):
    if request.method == "POST":
        disease_name = request.POST.get("disease_name")
        crop_name = request.POST.get("crop_name")
        case_notes = request.POST.get("case_notes")
        disease_key = request.POST.get("disease_key")
        
        if not disease_name or not crop_name:
            messages.error(request, 'Missing required fields.')
            return redirect('farmer_detect_disease')
        
        analysis = Analysis.objects.create(
            farmer=request.user,
            crop_name=crop_name,
            disease_name=disease_name,
        )
        
        case = Case.objects.create(
            farmer=request.user,
            analysis=analysis,
            title=f"Case for {crop_name} - {disease_name}",
            description=case_notes or f"Need help with {disease_name} on {crop_name}"
        )
        
        messages.success(request, f"Case #{case.id} opened successfully!")
        return redirect('farmer_case_detail', case_id=case.id)
    
    return redirect('farmer_detect_disease')
