from django.shortcuts import render


def landing_page(request):
    return render(request, 'landing.html')


def login_page(request):
    return render(request, 'auth/login.html')


def register_user_page(request):
    return render(request, 'auth/register/register_user.html')


def register_doctor_page(request):
    return render(request, 'auth/register/register_doctor.html')
