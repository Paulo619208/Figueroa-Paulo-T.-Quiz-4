from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from .models import Profile, CustomUser
from jobs.models import Job, JobApplicant


def signup_view(request):
    if request.user.is_authenticated:
        messages.info(request, 'You are already signed in.')
        # ✅ FIXED: Redirect to the correct homepage URL name
        return redirect('posts:post-list')

    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        # username is not in your CustomUser model, so we'll use email for it
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')

        # Simplified validation (Django Forms are better for this)
        if not all([email, password, confirm_password]):
            messages.error(request, 'All fields are required.')
            return render(request, 'auth/signup.html', {'email': email})

        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'auth/signup.html', {'email': email})

        try:
            # Create user
            user = CustomUser.objects.create_user(
                email=email.lower(),
                password=password
            )

            # ✅ IMPROVED: Automatically log the user in after they sign up
            login(request, user)

            messages.success(request, 'Account created successfully! Welcome.')
            # ✅ FIXED: Redirect to the posts page as requested
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
            # ✅ FIXED: Redirect to the posts page after a successful sign-in
            return redirect('posts:post-list')
        else:
            messages.error(request, 'Invalid email or password')

    return render(request, 'auth/signin.html')


def profile_edit_view(request):
    # This view is not yet implemented.
    # You would add form logic here to edit a user's profile.
    pass


def profile_view(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Please sign in first.')
        return redirect('auth:signin')

    # Use get_object_or_404 for cleaner code
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        # ✅ FIXED: Redirect to the correct profile edit/create URL
        messages.info(request, 'Please create your profile.')
        return redirect('auth:profile_edit')

    context = {'profile': profile}
    return render(request, 'auth/profile_view.html', context)


def logout_view(request):
    logout(request)
    messages.success(request, "You have been successfully logged out.")
    return redirect('auth:signin')