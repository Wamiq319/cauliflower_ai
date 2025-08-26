from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.core.paginator import Paginator
from django.http import JsonResponse
from .models import Case, Analysis, CaseSuggestion
import random
from apps.doctors.models import GeneralSuggestion  # Make sure this import is correct

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
            if case.status != 'closed':
                case.status = 'closed'
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
    case = get_object_or_404(Case, id=case_id, farmer=request.user)
    
    if request.method == 'POST':
        # Handle case closure
        if 'close_case' in request.POST:
            if case.status != 'closed':
                case.status = 'closed'
                case.save()
                messages.success(request, f'Case #{case.id} has been closed successfully.')
            else:
                messages.info(request, f'Case #{case.id} is already closed.')
            return redirect('farmer_case_detail', case_id=case.id)
        
        # Handle case reopening (if needed)
        elif 'reopen_case' in request.POST:
            if case.status == 'closed':
                case.status = 'open'
                case.save()
                messages.success(request, f'Case #{case.id} has been reopened.')
            else:
                messages.info(request, f'Case #{case.id} is already open.')
            return redirect('farmer_case_detail', case_id=case.id)
    
    # Get all suggestions for this case
    suggestions = case.suggestions.all().select_related('doctor')
    
    return render(request, 'dashboard/farmer/case_detail.html', {
        'case': case,
        'suggestions': suggestions
    })

@login_required
def farmer_close_case_ajax(request, case_id):
    """AJAX endpoint for closing a case"""
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        try:
            case = Case.objects.get(id=case_id, farmer=request.user)
            if case.status != 'closed':
                case.status = 'closed'
                case.save()
                return JsonResponse({
                    'success': True,
                    'message': f'Case #{case.id} closed successfully.',
                    'new_status': 'closed'
                })
            else:
                return JsonResponse({
                    'success': False,
                    'message': f'Case #{case.id} is already closed.'
                })
        except Case.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Case not found or access denied.'
            }, status=404)
    
    return JsonResponse({
        'success': False,
        'message': 'Invalid request method.'
    }, status=400)

# =============================================================================
# DISEASE DETECTION & CASE CREATION VIEWS
# =============================================================================

@login_required
def detect_disease_view(request):
    """Detect disease from uploaded plant image"""
    result = None
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
            "crop_name": "Cauliflower",
            "disease_name": disease_name,
            "analysis_date": timezone.now().strftime("%Y-%m-%d %H:%M"),
            "suggestions": suggestions,
            "disease_key": disease_key,
        }

    return render(request, "dashboard/farmer/image_upload.html", {"result": result})

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