# The views used below are normally mapped in django.contrib.admin.urls.py
# This URLs file is used to provide a reliable view deployment for test purposes.
# It is also provided as a convenience to those who want to deploy these URLs
# elsewhere.

from django.contrib.auth import views
from django.urls import path
from cabinet_contentkeys import views

urlpatterns = [
    path('site/<int:site_id>/contentkeys/add/', views.edit, name='cabinet_contentkeys_add'),
    path('site/<int:site_id>/contentkey/<int:contentkey_id>/edit/', views.edit, name='cabinet_contentkeys_edit'),
    path('site/<int:site_id>/contentkey/<int:contentkey_id>/delete/', views.delete, name='cabinet_contentkeys_delete'),
    path('site/<int:site_id>/contentkeys/', views.index, name='cabinet_contentkeys_index'),
]


