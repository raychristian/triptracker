from django.contrib.auth.backends import ModelBackend
from .models import UserProfile
from django.contrib.auth.models import User
import hashlib
import os

class DatastoreBackend(ModelBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):
        # Fetch the user by email from the datastore
        user_profile = UserProfile.query(UserProfile.email == username).get()

        if user_profile:
            # Check if the hashed password matches the one stored in the datastore
            hashed_password = self.hash_password(password, user_profile.salt)
            if hashed_password == user_profile.password:
                # Here, we're going to create a Django user object on-the-fly without saving it to the database
                user = User(username=user_profile.username, password=hashed_password, email=user_profile.email)
                user.id = user_profile.key.id()  # Set the ID of the Django user to the ID of the Datastore user
                return user

        return None

    def get_user(self, user_id):
        # Given a user ID, fetch the user from Datastore and return a Django user object
        user_profile = UserProfile.get_by_id(int(user_id))
        if user_profile:
            user = User(username=user_profile.username, email=user_profile.email)
            user.id = user_profile.key.id()
            return user
        return None

    @staticmethod
    def hash_password(password, salt):
        # Combine the password and salt, then hash the result
        salted_password = (password + salt).encode('utf-8')
        return hashlib.sha256(salted_password).hexdigest()
