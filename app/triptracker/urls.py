"""
URL mappings for triptracker

"""

from django.urls import path
from . import views

app_name = 'triptracker'

urlpatterns = [
    path("", views.home, name="home"),  # This will make the home view accessible at the base URL
    path("login/", views.login_request, name="login"),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path("myaccount/", views.myaccount_request, name="myaccount"),
    path("faq/", views.faq_view, name="faq"),
]
