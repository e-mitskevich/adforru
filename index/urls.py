# The views used below are normally mapped in django.contrib.admin.urls.py
# This URLs file is used to provide a reliable view deployment for test purposes.
# It is also provided as a convenience to those who want to deploy these URLs
# elsewhere.

from django.contrib.auth import views
from django.urls import path
from index import views

urlpatterns = [
    path('', views.home, name='index_home'),
    path('tracker', views.tracker, name='index_tracker'),
]


