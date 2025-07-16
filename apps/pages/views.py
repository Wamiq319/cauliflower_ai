from django.shortcuts import render


def landing_page(request):
    return render(request, 'landing.html')


def login_page(request):
    return render(request, 'auth/login.html')
