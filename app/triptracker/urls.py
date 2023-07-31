"""
URL mappings for triptracker

"""

from django.urls import path

from triptracker import views

app_name = 'triptracker'

urlpatterns = [
	path('',views.landing, name='landing'),	
]