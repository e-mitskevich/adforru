# The views used below are normally mapped in django.contrib.admin.urls.py
# This URLs file is used to provide a reliable view deployment for test purposes.
# It is also provided as a convenience to those who want to deploy these URLs
# elsewhere.

from django.contrib.auth import views
from django.urls import path
from cabinet import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='cabinet_sites'),
    path('login', views.login, name='cabinet_login'),
    path('logout', auth_views.logout, name='cabinet_logout'),
    path('registration', views.registration, name='cabinet_registration'),
]
