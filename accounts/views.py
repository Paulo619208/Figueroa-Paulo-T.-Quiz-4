from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from .models import Profile, CustomUser
from .forms import ProfileForm  # ✅ IMPORT THE NEW PROFILE FORM
from jobs.models import Job, JobApplicant


def signup_view(request):
    if request.user.is_authenticated:
        messages.info(request, 'You are already signed in.')
        return redirect('posts:post-list')

    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')

        if not all([email, password, confirm_password]):
            messages.error(request, 'All fields are required.')
            return render(request, 'auth/signup.html', {'email': email})

        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'auth/signup.html', {'email': email})

        try:
            user = CustomUser.objects.create_user(
                email=email.lower(),
                password=password
            )
            login(request, user)
            messages.success(request, 'Account created successfully! Welcome.')
            return redirect('posts:post-list')

        except (ValidationError, IntegrityError) as e:
            messages.error(request, f'An error occurred: {e}')
            return render(request, 'auth/signup.html', {'email': email})

    return render(request, 'auth/signup.html')


def signin_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('posts:post-list')
        else:
            messages.error(request, 'Invalid email or password')

    return render(request, 'auth/signin.html')


# ✅ FIXED: Replaced the empty view with the complete logic for creating/editing a profile.
@login_required
def profile_edit_view(request):
    # Get the user's profile, or create one if it doesn't exist
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('auth:profile')
    else:
        form = ProfileForm(instance=profile)

    context = {'form': form}
    return render(request, 'auth/profile_edit.html', context)


@login_required
def profile_view(request):
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        messages.info(request, 'Please create your profile.')
        return redirect('auth:profile_edit')

    context = {'profile': profile}
    return render(request, 'auth/profile_view.html', context)


def logout_view(request):
    logout(request)
    messages.success(request, "You have been successfully logged out.")
    return redirect('auth:signin')