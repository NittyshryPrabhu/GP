from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import UserProfile
from .forms import RegisterForm


# ---------------- REGISTER ----------------
def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data['email']
            user.save()

            # ✅ Profile is created automatically by signals

            # ✅ Update extra fields safely
            profile = user.userprofile
            profile.mobile = form.cleaned_data.get('mobile')
            profile.dob = form.cleaned_data.get('dob')
            profile.subscription = form.cleaned_data.get('subscription')
            profile.save()

            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('home')
    else:
        form = RegisterForm()

    return render(request, 'users/register.html', {'form': form})


# ---------------- LOGIN ----------------
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('home')
    else:
        form = AuthenticationForm()

    return render(request, 'users/login.html', {'form': form})


# ---------------- LOGOUT ----------------
def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('home')


# ---------------- PROFILE ----------------
@login_required
def profile_view(request):
    profile = request.user.userprofile   # ✅ safe (signal ensures existence)
    return render(request, 'users/profile.html', {'profile': profile})


# ---------------- EDIT PROFILE ----------------
@login_required
def edit_profile(request):
    profile = request.user.userprofile

    if request.method == 'POST':
        profile.bio = request.POST.get('bio')
        profile.mobile = request.POST.get('mobile')
        profile.dob = request.POST.get('dob')
        profile.subscription = request.POST.get('subscription')

        if request.FILES.get('avatar'):
            profile.avatar = request.FILES.get('avatar')

        profile.save()
        messages.success(request, "Profile updated successfully!")
        return redirect('profile')

    return render(request, 'users/edit_profile.html', {'profile': profile})
