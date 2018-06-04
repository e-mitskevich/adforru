# The views used below are normally mapped in django.contrib.admin.urls.py
# This URLs file is used to provide a reliable view deployment for test purposes.
# It is also provided as a convenience to those who want to deploy these URLs
# elsewhere.

from django.contrib.auth import views
from django.urls import path
from cabinet_sites import views

urlpatterns = [
    path('site/<int:site_id>/', views.show, name='cabinet_sites_show'),
    path('sites/add/', views.edit, name='cabinet_sites_add'),
    path('site/<int:site_id>/edit/', views.edit, name='cabinet_sites_edit'),
    path('site/<int:site_id>/delete/', views.delete, name='cabinet_sites_delete'),
    path('sites/', views.index, name='cabinet_sites_index'),

    path('site/<int:site_id>/hypercontent.js', views.hypercontent_js, name='cabinet_sites_hypercontent_js'),
    path('site/<int:site_id>/conversion.js', views.conversion_js, name='cabinet_sites_conversion_js')
]


