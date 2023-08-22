import os
from .models import UserProfile, UserGeneratedVideo, AIAvatarVideo, VideoSession, AIAnalysis
from triptracker.authentication_backend import DatastoreBackend


def create_new_user(username, email, password):
    """
    Create a new user and save to Datastore.
    """
    salt = os.urandom(16).hex()
    hashed_password = DatastoreBackend.hash_password(password, salt)
    user = UserProfile(username=username, email=email, password=hashed_password, salt=salt)
    user_key = user.put()
    return user_key

def fetch_user_by_email(email):
    """
    Retrieve a user by their email.
    """
    user = UserProfile.query(UserProfile.email == email).get()
    return user

def create_new_video(user_id, videoURL, videoType, title=None, description=None):
    """
    Create a new user-generated video and save to Datastore.
    """
    video = UserGeneratedVideo(user_id=ndb.Key('UserProfile', user_id), videoURL=videoURL, videoType=videoType, title=title, description=description)
    video_key = video.put()
    return video_key

def get_recent_videos(limit=10):
    """
    Retrieve the recent videos.
    """
    recent_videos = UserGeneratedVideo.query().order(-UserGeneratedVideo.timestamp).fetch(limit)
    return recent_videos
