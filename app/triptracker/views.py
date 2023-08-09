from django.shortcuts import render
from django.shortcuts import render, redirect
from .forms import NewUserForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.conf import settings
import os


from django.templatetags.static import static
from django.urls import reverse


def dashboard(request):
    videos = [
        {
            "path": 'triptracker/recorded_videos/1stTripTrackerVid.webm',
        },
        {
            "path": 'triptracker/recorded_videos/2ndTripTrackerVid.webm',
        },
        {
            "path": 'triptracker/recorded_videos/3rdTripTrackerVid.webm',
        },
    ]

    context = {'videos': videos}
    return render(request, 'triptracker/dashboard.html', context)


def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        print(form.data)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful." )
            return redirect("home")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render (request=request, template_name="triptracker/register.html", context={"register_form":form})

def home(request):
    return render(request, "triptracker/home.html")

def login_request(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        print(f"Attempting to authenticate user {username}")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            print(f"User object: {request.user}") 
            print(f"User {username} is authenticated: {request.user.is_authenticated}")
            return redirect('home') # or wherever you want to redirect after login
        else:
            print(f"Authentication failed for user {username}") 
            return render(request, "registration/login.html", {
                "message": "Invalid username or password."
            })
    return render(request, "registration/login.html")


def logout_view(request):
    logout(request)
    return redirect('/')  # Redirect to a success page.


def myaccount_request(request):
    return render(request, 'triptracker/myaccount.html')


def faq_view(request):
    return render(request, 'triptracker/faq.html')
