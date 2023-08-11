"""
Datastore ndb models
"""

from google.cloud import ndb


class UserProfile(ndb.Model):
	# User's registration info

    userID = ndb.KeyProperty()  # Unique identifier for each user.
    username = ndb.StringProperty()  # User's display name.
    email = ndb.StringProperty()  # User's email address.
    password = ndb.StringProperty()  # Encrypted password for authentication. NOTE: Consider hashing.
    registrationDate = ndb.DateTimeProperty(auto_now_add=True)  # Registration date and time.
    videoIDs = ndb.KeyProperty(kind='UserGeneratedVideo', repeated=True)  # Video IDs linked to the user.


class UserGeneratedVideo(ndb.Model):
	# User's video responses 

    videoID = ndb.KeyProperty()  # Unique video identifier.
    userID = ndb.KeyProperty(kind='UserProfile')  # Reference to the associated user.
    videoURL = ndb.StringProperty()  # Link to the video storage location.
    videoType = ndb.StringProperty()  # Type of video (e.g., AV, UPV, AAV, AHV).
    timestamp = ndb.DateTimeProperty(auto_now_add=True)  # Video upload or creation date/time.
    duration = ndb.IntegerProperty()  # Video duration (in seconds).
    title = ndb.StringProperty()  # (Optional) Video title.
    description = ndb.StringProperty()  # (Optional) Video description.
    shareable = ndb.BooleanProperty(default=False)  # If the video can be shared.
    analysisReference = ndb.KeyProperty(kind='AIAnalysis')  # Key/Reference to the associated AIAnalysis Entity.


class AIAvatarVideo(ndb.Model):
	# Pre-recorded AI prompt videos

    videoID = ndb.KeyProperty()  # Unique video identifier.
    sessionID = ndb.KeyProperty(kind='VideoSession')  # Reference to the related user session.
    videoURL = ndb.StringProperty()  # Link to the video storage location.
    videoType = ndb.StringProperty()  # Type of avatar video (e.g., Greeting, Topic Prompt).
    timestamp = ndb.DateTimeProperty(auto_now_add=True)  # Video upload or creation date/time.
    duration = ndb.IntegerProperty()  # Video duration (in seconds).
    title = ndb.StringProperty()  # Title or purpose of the avatar video (e.g., "Greeting").
    description = ndb.StringProperty()  # A brief description or context for the avatar video.


class VideoSession(ndb.Model):
	# A full session of user video responses 

    sessionID = ndb.KeyProperty()  # Unique session identifier.
    userID = ndb.KeyProperty(kind='UserProfile')  # Reference to the participating user.
    videoSequence = ndb.KeyProperty(kind='UserGeneratedVideo', repeated=True)  # Video IDs sequence for the session.
    sessionTitle = ndb.StringProperty()  # (Optional) Session title.
    sessionDescription = ndb.StringProperty()  # (Optional) Session description.
    shareable = ndb.BooleanProperty(default=False)  # If the session can be shared.


class AIAnalysis(ndb.Model):
	# A custom video with AI analysis of a user's previous video response

    analysisID = ndb.KeyProperty()  # Unique analysis identifier.
    videoID = ndb.KeyProperty(kind='UserGeneratedVideo')  # Reference to the analyzed video.
    summaryText = ndb.StringProperty()  # AI analysis summary.
    responseScript = ndb.StringProperty()  # Detailed AI response.
    shareable = ndb.BooleanProperty(default=False)  # If the analysis can be shared.
    keywords = ndb.StringProperty(repeated=True)  # List of key terms or topics.
    sentimentScore = ndb.IntegerProperty()  # Numeric score representing the overall sentiment.
    mainThemes = ndb.StringProperty(repeated=True)  # List of primary themes in the video.


