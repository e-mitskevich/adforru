"""adfor URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin, auth
from django.contrib.auth import urls
from django.urls import path, include

urlpatterns = [
    path("", include("index.urls")),
    path('admin/', admin.site.urls),
    path('cabinet/', include('cabinet.urls')),
    path('cabinet/', include('cabinet_sites.urls')),
    path('cabinet/', include('cabinet_tags.urls')),
    path('cabinet/', include('cabinet_contentkeys.urls'))
]
