from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.utils.http import url_has_allowed_host_and_scheme
from django.contrib import messages
from .models import User


def register(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')
        role = request.POST.get('role', 'doctor')
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()

        if not username:
            messages.error(request, 'Username is required!')
            return redirect('register')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match!')
            return redirect('register')

        # Validate password strength against Django validators
        try:
            validate_password(password)
        except ValidationError as e:
            for error in e.messages:
                messages.error(request, error)
            return redirect('register')

        if User.objects.filter(username__iexact=username).exists():
            messages.error(request, 'Username already exists! Please choose another.')
            return redirect('register')

        if email and User.objects.filter(email__iexact=email).exists():
            messages.error(request, 'An account with this email already exists!')
            return redirect('register')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            role=role,
            first_name=first_name,
            last_name=last_name
        )
        messages.success(request, f'Account created for Dr. {user.username}! Please sign in below.')
        return redirect('login')

    return render(request, 'accounts/register.html')


def user_login(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    next_url = request.GET.get('next') or request.POST.get('next')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
                return redirect(next_url)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password! Please verify your credentials or register a new account.')
            return render(request, 'accounts/login.html', {'next': next_url})

    return render(request, 'accounts/login.html', {'next': next_url})


@login_required
def user_logout(request):
    logout(request)
    messages.success(request, 'You have been successfully signed out.')
    return redirect('login')
