from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from apps.accounts.models import CustomUser
from apps.admin_panel.models import Event

# Helper to restrict access
def is_admin(user):
    return user.role == 'admin'

# -----------------------------------------------------------------------------
# ADMIN DASHBOARD
# -----------------------------------------------------------------------------
@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    """Admin dashboard with stats overview."""
    return render(request, "dashboard/admin/dashboard.html", {
        "user": request.user,
        "users": CustomUser.objects.filter(is_staff=False, is_superuser=False, role='farmer').count(),
        "doctors": CustomUser.objects.filter(role='doctor').count(),
    })

# -----------------------------------------------------------------------------
# MANAGE EVENTS
# -----------------------------------------------------------------------------
@login_required
@user_passes_test(is_admin)
def manage_events(request):
    """Display all events and allow adding new ones."""
    events = Event.objects.all()
    return render(request, "dashboard/admin/manage_events.html", {
        "user": request.user,
        "events": events,
    })

# -----------------------------------------------------------------------------
# MANAGE FARMERS
# -----------------------------------------------------------------------------
@login_required
@user_passes_test(is_admin)
def manage_farmers(request):
    """List all farmer users."""
    farmers = CustomUser.objects.filter(role='farmer')
    return render(request, "dashboard/admin/manage_farmers.html", {
        "user": request.user,
        "farmers": farmers,
    })

# -----------------------------------------------------------------------------
# MANAGE DOCTORS
# -----------------------------------------------------------------------------
@login_required
@user_passes_test(is_admin)
def manage_doctors(request):
    """List all doctors."""
    doctors = CustomUser.objects.filter(role='doctor')
    return render(request, "dashboard/admin/manage_doctors.html", {
        "user": request.user,
        "doctors": doctors,
    })

# -----------------------------------------------------------------------------
# APPROVE REQUESTS
# -----------------------------------------------------------------------------
@login_required
@user_passes_test(is_admin)
def approve_requests(request):
    """Approve or reject new user registration requests."""
    # For now, we'll show all users that might need approval
    # In a real system, you might have a separate model for pending requests
    pending_users = CustomUser.objects.filter(is_active=False)
    
    if request.method == "POST":
        user_id = request.POST.get("user_id")
        action = request.POST.get("action")  # 'approve' or 'reject'
        
        try:
            user = CustomUser.objects.get(id=user_id)
            if action == 'approve':
                user.is_active = True
                user.save()
                messages.success(request, f"User {user.username} has been approved.")
            elif action == 'reject':
                user.delete()
                messages.success(request, f"User {user.username} has been rejected and deleted.")
        except CustomUser.DoesNotExist:
            messages.error(request, "User not found.")
    
    return render(request, "dashboard/admin/approve_requests.html", {
        "user": request.user,
        "pending_users": pending_users,
    })

# -----------------------------------------------------------------------------
# ADMIN PROFILE
# -----------------------------------------------------------------------------
@login_required
@user_passes_test(is_admin)
def admin_profile(request):
    """Admin profile update page."""
    user = request.user

    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")

        if name:
            user.first_name = name
        if email:
            user.email = email
        user.save()

        messages.success(request, "Profile updated successfully!")

    return render(request, "dashboard/admin/profile.html", {
        "user": user
    })
