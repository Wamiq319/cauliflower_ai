# views.py
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib import messages
from .models import FarmerProfile, DoctorProfile 
from django.contrib.auth import authenticate, login


User = get_user_model()

def register_user(request):
    if request.method == 'POST':
        username = request.POST.get('username').strip()
        email = request.POST.get('email').strip()
        password = request.POST.get('password')
        first_name = request.POST.get('first_name').strip()
        last_name = request.POST.get('last_name').strip()
        farm_size = request.POST.get('farm_size')
        years_farming = request.POST.get('years_farming')
        main_crops = request.POST.get('main_crops').strip()
        irrigation_method = request.POST.get('irrigation_method').strip()

        # Basic checks
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('register_user')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return redirect('register_user')

        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            role='farmer'
        )

        # Create farmer profile
        FarmerProfile.objects.create(
            user=user,
            farm_size=farm_size,
            years_farming=years_farming,
            main_crops=main_crops,
            irrigation_method=irrigation_method
        )

        messages.success(request, 'Registration successful! Please log in.')
        return redirect('login')  # Redirect to login page after success

    return render(request, 'auth/register/register_user.html')

def register_doctor(request):
    if request.method == 'POST':
        username = request.POST.get('username').strip()
        email = request.POST.get('email').strip()
        password = request.POST.get('password')
        first_name = request.POST.get('first_name').strip()
        last_name = request.POST.get('last_name').strip()
        specialization = request.POST.get('specialization').strip()

        # Basic checks
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('register_doctor')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return redirect('register_doctor')

        # Create doctor user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            role='doctor',
          
        )

        # Create doctor profile
        DoctorProfile.objects.create(
            user=user,
            specialization=specialization
        )

        messages.success(request, 'Doctor account created successfully! Please log in.')
        return redirect('login')  # Go to login page after registration

    return render(request, 'auth/register/register_doctor.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username').strip()
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # Redirect based on role
            if user.role == 'farmer':
                return redirect('/dashboard/farmer/')
            elif user.role == 'doctor':
                return redirect('/dashboard/doctor/')
            elif user.role == 'admin':
                return redirect('/admin/')
            else:
                return redirect('/')  # default fallback
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'auth/login.html')
