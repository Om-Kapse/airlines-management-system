from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from .forms import SignupForm, LoginForm

def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # will make home later
    else:
        form = SignupForm()
    return render(request, 'users/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

@login_required
def admin_dashboard(request):
    return HttpResponse("Welcome Admin! Manage flights, airplanes, and reports here.")

@login_required
def staff_dashboard(request):
    return HttpResponse("Welcome Staff! Handle check-ins and passenger support here.")

@login_required
def passenger_dashboard(request):
    return render(request, "users/passenger_dashboard.html")

@login_required
def admin_dashboard(request):
    return redirect("admin_flights_dashboard")
