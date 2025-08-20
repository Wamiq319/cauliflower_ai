from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import GeneralSuggestion

@login_required
def create_suggestion(request):
    if request.method == "POST":
        disease_type = request.POST.get("disease_type")
        title = request.POST.get("title")
        treatment = request.POST.get("treatment")
        prevention = request.POST.get("prevention")
        best_practices = request.POST.get("best_practices")
        priority = request.POST.get("priority")

        # Save suggestion
        GeneralSuggestion.objects.create(
            doctor=request.user,
            disease_type=disease_type,
            title=title,
            treatment=treatment,
            prevention=prevention,
            best_practices=best_practices,
            priority=priority,
        )
        return redirect("doctor_past_suggestions")  # after saving, go to list page

    return render(request, "dashboard/doctor/create_suggestion.html")
