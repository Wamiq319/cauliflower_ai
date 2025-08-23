from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from apps.accounts.models import CustomUser
from .models import Event
from datetime import datetime

# -----------------------------------------------------------------------------
# EVENTS MANAGEMENT
# -----------------------------------------------------------------------------
def manage_events(request):
    """Display all events and allow adding new ones."""
    events = Event.objects.all()
    return render(request, 'dashboard/admin/manage_events.html', {
        'events': events
    })

@csrf_exempt
def add_event(request):
    """Add a new event."""
    if request.method == 'POST':
        try:
            title = request.POST.get('title', '').strip()
            date_str = request.POST.get('date', '').strip()
            venue = request.POST.get('venue', '').strip()
            description = request.POST.get('description', '').strip()
            
            # Validation
            if not all([title, date_str, venue, description]):
                messages.error(request, 'All fields are required.')
                return JsonResponse({'success': False, 'message': 'All fields are required.'})
            
            # Parse date
            try:
                date = datetime.strptime(date_str, '%Y-%m-%d').date()
            except ValueError:
                messages.error(request, 'Invalid date format. Use YYYY-MM-DD.')
                return JsonResponse({'success': False, 'message': 'Invalid date format. Use YYYY-MM-DD.'})
            
            # Create event
            event = Event.objects.create(
                title=title,
                date=date,
                venue=venue,
                description=description
            )
            
            messages.success(request, f'Event "{title}" has been successfully created.')
            return JsonResponse({'success': True, 'message': f'Event "{title}" created successfully.'})
            
        except Exception as e:
            messages.error(request, f'Error creating event: {str(e)}')
            return JsonResponse({'success': False, 'message': f'Error creating event: {str(e)}'})
    
    return JsonResponse({'success': False, 'message': 'Invalid request method.'})

@csrf_exempt
def edit_event(request, event_id):
    """Edit an existing event."""
    if request.method == 'POST':
        try:
            event = get_object_or_404(Event, id=event_id)
            
            title = request.POST.get('title', '').strip()
            date_str = request.POST.get('date', '').strip()
            venue = request.POST.get('venue', '').strip()
            description = request.POST.get('description', '').strip()
            
            # Validation
            if not all([title, date_str, venue, description]):
                messages.error(request, 'All fields are required.')
                return JsonResponse({'success': False, 'message': 'All fields are required.'})
            
            # Parse date
            try:
                date = datetime.strptime(date_str, '%Y-%m-%d').date()
            except ValueError:
                messages.error(request, 'Invalid date format. Use YYYY-MM-DD.')
                return JsonResponse({'success': False, 'message': 'Invalid date format. Use YYYY-MM-DD.'})
            
            # Update event
            event.title = title
            event.date = date
            event.venue = venue
            event.description = description
            event.save()
            
            messages.success(request, f'Event "{title}" has been successfully updated.')
            return JsonResponse({'success': True, 'message': f'Event "{title}" updated successfully.'})
            
        except Exception as e:
            messages.error(request, f'Error updating event: {str(e)}')
            return JsonResponse({'success': False, 'message': f'Error updating event: {str(e)}'})
    
    return JsonResponse({'success': False, 'message': 'Invalid request method.'})

@csrf_exempt
def delete_event(request, event_id):
    """Delete an event."""
    if request.method == 'POST':
        try:
            event = get_object_or_404(Event, id=event_id)
            event_title = event.title
            event.delete()
            messages.success(request, f'Event "{event_title}" has been successfully deleted.')
            return JsonResponse({'success': True, 'message': f'Event "{event_title}" deleted successfully.'})
        except Exception as e:
            messages.error(request, f'Error deleting event: {str(e)}')
            return JsonResponse({'success': False, 'message': f'Error deleting event: {str(e)}'})
    
    return JsonResponse({'success': False, 'message': 'Invalid request method.'})

# -----------------------------------------------------------------------------
# DELETE DOCTOR
# -----------------------------------------------------------------------------
@csrf_exempt
def delete_doctor(request, doctor_id):
    """Delete a doctor account."""
    if request.method == 'POST':
        try:
            doctor = get_object_or_404(CustomUser, id=doctor_id, role='doctor')
            doctor_name = f"{doctor.first_name} {doctor.last_name}".strip() or doctor.username
            doctor.delete()
            messages.success(request, f'Doctor "{doctor_name}" has been successfully deleted.')
            return JsonResponse({'success': True, 'message': f'Doctor "{doctor_name}" deleted successfully.'})
        except Exception as e:
            messages.error(request, f'Error deleting doctor: {str(e)}')
            return JsonResponse({'success': False, 'message': f'Error deleting doctor: {str(e)}'})
    
    return JsonResponse({'success': False, 'message': 'Invalid request method.'})

# -----------------------------------------------------------------------------
# DELETE FARMER
# -----------------------------------------------------------------------------
@csrf_exempt
def delete_farmer(request, farmer_id):
    """Delete a farmer account."""
    if request.method == 'POST':
        try:
            farmer = get_object_or_404(CustomUser, id=farmer_id, role='farmer')
            farmer_name = f"{farmer.first_name} {farmer.last_name}".strip() or farmer.username
            farmer.delete()
            messages.success(request, f'Farmer "{farmer_name}" has been successfully deleted.')
            return JsonResponse({'success': True, 'message': f'Farmer "{farmer_name}" deleted successfully.'})
        except Exception as e:
            messages.error(request, f'Error deleting farmer: {str(e)}')
            return JsonResponse({'success': False, 'message': f'Error deleting farmer: {str(e)}'})
    
    return JsonResponse({'success': False, 'message': 'Invalid request method.'})

# -----------------------------------------------------------------------------
# UPDATE ADMIN PROFILE
# -----------------------------------------------------------------------------
@csrf_exempt
def update_admin_profile(request):
    """Update admin profile information."""
    if request.method == 'POST':
        try:
            admin = request.user
            
            # Update basic information
            first_name = request.POST.get('first_name', '').strip()
            last_name = request.POST.get('last_name', '').strip()
            email = request.POST.get('email', '').strip()
            
            if first_name:
                admin.first_name = first_name
            if last_name:
                admin.last_name = last_name
            if email:
                admin.email = email
            
            # Update password if provided
            new_password = request.POST.get('new_password', '').strip()
            confirm_password = request.POST.get('confirm_password', '').strip()
            
            if new_password and confirm_password:
                if new_password == confirm_password:
                    if len(new_password) >= 6:
                        admin.set_password(new_password)
                        admin.plain_password = new_password
                        messages.success(request, 'Password updated successfully.')
                    else:
                        messages.error(request, 'Password must be at least 6 characters long.')
                        return JsonResponse({'success': False, 'message': 'Password must be at least 6 characters long.'})
                else:
                    messages.error(request, 'Passwords do not match.')
                    return JsonResponse({'success': False, 'message': 'Passwords do not match.'})
            
            admin.save()
            messages.success(request, 'Admin profile updated successfully.')
            return JsonResponse({'success': True, 'message': 'Admin profile updated successfully.'})
            
        except Exception as e:
            messages.error(request, f'Error updating admin profile: {str(e)}')
            return JsonResponse({'success': False, 'message': f'Error updating admin profile: {str(e)}'})
    
    return JsonResponse({'success': False, 'message': 'Invalid request method.'})
