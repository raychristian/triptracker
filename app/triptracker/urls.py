"""
URL mappings for triptracker

"""

from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


app_name = 'triptracker'

urlpatterns = [
    path("", views.home, name="home"),  # This will make the home view accessible at the base URL
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register_request, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path("myaccount/", views.myaccount_request, name="myaccount"),
    path("faq/", views.faq_view, name="faq"),
    path('get_signed_url/', views.get_signed_url, name='get_signed_url'),
    path('password_check/', views.password_check, name='password_check'),
]
