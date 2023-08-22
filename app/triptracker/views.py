from django.shortcuts import render
from django.shortcuts import render, redirect
from .forms import NewUserForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.conf import settings
import os

from .services import create_new_user

from django.templatetags.static import static
from django.urls import reverse

from google.cloud import storage
from django.http import JsonResponse

from triptracker.models import UserGeneratedVideo
from google.cloud import ndb
import datetime
import uuid


def get_signed_url(request):
    if request.method == 'POST':
        # Authentication and authorization checks...

        # Generate a signed URL for uploading to GCS
        storage_client = storage.Client()
        bucket = storage_client.get_bucket('triptracker-394521.appspot.com')
        blob = bucket.blob('videos/' + str(request.user.id) + '/video_filename.webm')
        
        # Generate a signed URL for this blob that lasts for 300 seconds (5 minutes)
        signed_url = blob.generate_signed_url(expiration=300, method='PUT')
        
        # Return the signed URL to the client
        return JsonResponse({'signed_url': signed_url})

    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)


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
            print(request.session.session_key)
            print(f"User object: {request.user}") 
            print(f"User {username} is authenticated: {request.user.is_authenticated}")
            return redirect('triptracker:home') # or wherever you want to redirect after login
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

def save_video_metadata(user_id, video_url):
    """
    Save metadata about a user's video recording in Google Cloud Datastore.
    
    Parameters:
        user_id (str): The ID of the user who created the video.
        video_url (str): The URL of the video in Google Cloud Storage.
        Add additional fields (from models.py) later
    """
    
    with ndb.Client().context():
        # Create a new UserGeneratedVideo entity
        user_video = UserGeneratedVideo(
            user_id=ndb.Key('UserProfile', user_id),
            videoID = ndb.StringProperty(default=lambda: str(uuid.uuid4())),
            videoURL=video_url,
            timestamp=datetime.datetime.now()  # Automatically set the current date and time
        )
        # Save the entity to Datastore
        user_video.put()
    
    print('Saved video metadata for user:', user_id)


