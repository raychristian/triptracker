from django.shortcuts import render
from django.shortcuts import render, redirect
from .forms import NewUserForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.conf import settings
import os

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from google.cloud import storage
from triptracker.models import UserGeneratedVideoEntity

from .services import create_new_user

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
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        user_key = create_new_user(username, email, password)
        if user_key:
            messages.success(request, "Registration successful.")
            return redirect("triptracker:home")
        else:
            messages.error(request, "Unsuccessful registration. Invalid information.")
    return render(request, "triptracker/register.html") # Or whichever template you're using for registration



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


@csrf_exempt
def save_video(request):
    if request.method == 'POST':
        video_file = request.FILES['video']
        user_id = request.POST.get('user_id', None)
        
        # Save to Google Cloud Storage
        storage_client = storage.Client()
        bucket_name = 'triptracker-394521'
        bucket = storage_client.bucket(bucket_name)
        
        blob = bucket.blob(video_file.name)
        blob.upload_from_file(video_file.file, content_type=video_file.content_type)
        video_url = blob.public_url
        
        # Save reference to Google Cloud Datastore
        video = UserGeneratedVideoEntity(
            videoID=ndb.Key('UserGeneratedVideo', video_file.name),  
            userID=ndb.Key('UserProfile', user_id),
            videoURL=video_url,
            videoType='UPV',
            duration=0,  # Future product feature (pull from front end)
            title="Sample Video Title",  # Future product feature (pull from front end)
            description="Sample Video Description",  # Future product feature (pull from front end)
            shareable=False,  # Default to False (pull from frontend)
            analysisReference=None
        )
        video.save()
        
        return JsonResponse({'status': 'success', 'video_url': video_url})
        
    else:
        return JsonResponse({'status': 'fail', 'message': 'Invalid request method'}, status=400)
