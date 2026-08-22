from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import StudentRegistrationForm, ProfileUpdateForm
from .models import StudentProfile
from materials.models import ClassLevel

def register(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            class_level = form.cleaned_data.get('class_level')
            StudentProfile.objects.create(user=user, class_level=class_level)
            messages.success(request, 'Registration successful! Please login.')
            return redirect('login')
    else:
        form = StudentRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

def user_login(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'accounts/login.html')

@login_required
def user_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('home')

@login_required
def profile(request):
    profile, created = StudentProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=profile)
    return render(request, 'accounts/profile.html', {'form': form, 'profile': profile})
