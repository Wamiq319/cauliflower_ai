from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Case, Analysis,CaseMessage
import random
from apps.doctors.models import GeneralSuggestion  # Make sure this import is correct
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
# GLOBAL DISEASE DATA
# =============================================================================
DISEASE_GLOBAL_DATA = {
    "black_rot": {
        "prevention": [
            "Seedling Stage: Sterilize trays and pots",
            "Ensure seedlings are disease-free",
            "Maintain proper spacing",
            "Vegetative Stage: Prune affected leaves",
            "Avoid shaded or damp areas",
            "Use mulch",
            "Flowering Stage: Avoid overhead watering",
            "Monitor humidity",
            "Ventilate greenhouse",
            "Fruiting Stage: Remove infected fruits",
            "Rotate crops",
        ],
        "treatment": [
            "Seedling Stage: Spray copper-based fungicide weekly if infection detected",
            "Remove infected seedlings",
            "Vegetative Stage: Apply fungicide to affected areas",
            "Prune infected leaves",
            "Flowering Stage: Spray fungicide early morning or evening",
            "Remove infected flowers",
            "Fruiting Stage: Systemic fungicide",
            "Monitor fruits daily",
        ],
        "best_practices": [
            "Inspect plants daily",
            "Maintain clean tools",
            "Record outbreaks for future management",
        ],
    },
    "downy_mildew": {
        "prevention": [
            "Seedling Stage: Plant in sunny, ventilated areas",
            "Avoid water on leaves",
            "Vegetative Stage: Avoid dense planting",
            "Do not irrigate at night",
            "Flowering Stage: Keep humidity below 70%",
            "Remove affected leaves",
            "Fruiting Stage: Use drip irrigation",
            "Harvest promptly",
        ],
        "treatment": [
            "Seedling Stage: Spray neem oil if yellowing detected",
            "Vegetative Stage: Apply fungicide weekly",
            "Flowering Stage: Targeted fungicide early morning/evening",
            "Fruiting Stage: Remove infected fruits",
            "Apply protective fungicide",
        ],
        "best_practices": [
            "Inspect plants twice a week",
            "Ensure soil drains well",
            "Maintain proper crop rotation",
        ],
    },
    "bacterial_spot_rot": {
        "prevention": [
            "Seedling Stage: Use certified disease-free seeds",
            "Sanitize trays and tools",
            "Vegetative Stage: Avoid overhead irrigation",
            "Remove infected leaves",
            "Flowering Stage: Avoid working when leaves are wet",
            "Fruiting Stage: Rotate crops",
            "Disinfect harvesting tools",
        ],
        "treatment": [
            "Seedling Stage: Apply copper-based bactericide weekly",
            "Vegetative Stage: Spot spray infected leaves",
            "Flowering Stage: Spray bactericide early morning/evening",
            "Fruiting Stage: Remove infected fruits",
            "Apply systemic bactericide",
        ],
        "best_practices": [
            "Keep greenhouse ventilated",
            "Monitor humidity",
            "Maintain detailed records of outbreaks",
        ],
    },
}

# =============================================================================
# CASE MANAGEMENT VIEWS
# =============================================================================

@login_required
def farmer_cases_list(request):
    """Display all cases opened by the farmer in a table"""
    cases = Case.objects.filter(farmer=request.user).select_related('analysis').order_by('-created_at')
    
    # Handle case closure from list view
    if request.method == 'POST' and 'close_case' in request.POST:
        case_id = request.POST.get('case_id')
        try:
            case = Case.objects.get(id=case_id, farmer=request.user)
            if case.status != 'resolved':
                case.status = 'resolved'
                case.save()
                messages.success(request, f'Case #{case.id} has been closed successfully.')
            else:
                messages.info(request, f'Case #{case.id} is already closed.')
        except Case.DoesNotExist:
            messages.error(request, 'Case not found or you do not have permission to close it.')
        return redirect('farmer_cases_list')
    
    return render(request, 'dashboard/farmer/cases_list.html', {
        'cases': cases,
        'cases_count': cases.count()
    })


@login_required
def farmer_case_detail(request, case_id):
    """Display detailed view of a specific case with option to close it"""
    # Get the case with all related data including analysis and image
    case = get_object_or_404(
        Case.objects.select_related('analysis').prefetch_related('suggestions__doctor'),
        id=case_id, 
        farmer=request.user
    )
    
    # Print all case and disease information
    print(f"=== CASE DETAILS ===")
    print(f"Case ID: #{case.id}")
    print(f"Case Title: {case.title}")
    print(f"Case Status: {case.status}")
    print(f"Case Priority: {case.priority}")
    print(f"Case Description: {case.description}")
    print(f"Created: {case.created_at}")
    print(f"Updated: {case.updated_at}")
    
    print(f"\n=== DISEASE ANALYSIS ===")
    print(f"Crop: {case.analysis.crop_name}")
    print(f"Disease: {case.analysis.disease_name}")
    print(f"Analysis Date: {case.analysis.analysis_date}")
    if case.analysis.image:
        print(f"Image Path: {case.analysis.image.path}")
        print(f"Image URL: {case.analysis.image.url}")
        print(f"Image Name: {case.analysis.image.name}")
    else:
        print(f"Image: No image attached")
    
    print(f"\n=== FARMER INFO ===")
    print(f"Farmer: {case.farmer.username} ({case.farmer.first_name} {case.farmer.last_name})")
    
    print(f"\n=== SUGGESTIONS ===")
    suggestions = case.suggestions.all().select_related('doctor')
    print(f"Total Suggestions: {suggestions.count()}")
    for i, suggestion in enumerate(suggestions, 1):
        print(f"  {i}. By Dr. {suggestion.doctor.first_name} {suggestion.doctor.last_name}")
        print(f"     Title: {suggestion.title}")
        print(f"     Created: {suggestion.created_at}")
    
    if request.method == 'POST':
        # Handle case closure
        if 'close_case' in request.POST:
            if case.status != 'resolved':
                case.status = 'resolved'
                case.save()
                print(f"\n=== CASE STATUS UPDATE ===")
                print(f"Case #{case.id} marked as RESOLVED")
                messages.success(request, f'Case #{case.id} has been closed successfully.')
            else:
                print(f"\n=== CASE STATUS UPDATE ===")
                print(f"Case #{case.id} is already resolved")
                messages.info(request, f'Case #{case.id} is already closed.')
            return redirect('farmer_case_detail', case_id=case.id)
    
    return render(request, 'dashboard/farmer/case_detail.html', {
        'case': case,
        'suggestions': suggestions
    })

# =============================================================================
# DISEASE DETECTION & CASE CREATION VIEWS
# =============================================================================

@login_required
def detect_disease_view(request):
    """Detect disease from uploaded plant image"""
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

        # Fetch related suggestions
        suggestions_qs = GeneralSuggestion.objects.filter(
            disease_type=disease_key
        ).select_related("doctor")

        suggestions = []
        for s in suggestions_qs:
            doctor = s.doctor
            doctor_name = f"{doctor.first_name} {doctor.last_name}".strip()
            doctor_list.append({
                "id": doctor.id,
                "name": doctor_name,
            })
            if not doctor_name:
                doctor_name = doctor.username

            suggestions.append({
                "title": s.title,
                "treatment": s.treatment,
                "prevention": s.prevention,
                "best_practices": s.best_practices,
                "priority": s.priority,
                "suggested_by": doctor_name,
            })

        # Build result object
        result = {
            "disease_name": disease_name,
            "analysis_date": timezone.now().strftime("%Y-%m-%d %H:%M"),
            "suggestions": suggestions,
            "disease_key": disease_key,
            "general_info": DISEASE_GLOBAL_DATA.get(disease_key, {})
        }

    return render(request, "dashboard/farmer/image_upload.html", {"result": result, "doctor_list": doctor_list})

@login_required
def open_case_view(request):
    """Open a new case based on analysis results"""
    if request.method == "POST":
        disease_name = request.POST.get("disease_name")
        crop_name = request.POST.get("crop_name")
        case_notes = request.POST.get("case_notes")
        disease_key = request.POST.get("disease_key")
        
        # Validate required fields
        if not disease_name or not crop_name:
            messages.error(request, 'Missing required fields.')
            return redirect('farmer_detect_disease')
        
        # Create analysis record
        analysis = Analysis.objects.create(
            farmer=request.user,
            crop_name=crop_name,
            disease_name=disease_name,
        )
        
        # Determine priority based on disease severity
        priority = 'medium'
        urgent_diseases = ['black_rot', 'bacterial_spot_rot']
        if disease_key in urgent_diseases:
            priority = 'high'
        
        # Create case
        case = Case.objects.create(
            farmer=request.user,
            analysis=analysis,
            title=f"Case for {crop_name} - {disease_name}",
            description=case_notes or f"Need help with {disease_name} on {crop_name}",
            priority=priority,
            status='open'
        )
        
        messages.success(request, f"Case #{case.id} opened successfully! A doctor will review your {crop_name} case with {disease_name}.")
        return redirect('farmer_case_detail', case_id=case.id)
    
    return redirect('farmer_detect_disease')