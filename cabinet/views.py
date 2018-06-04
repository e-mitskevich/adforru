from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.forms import modelform_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.template import RequestContext
from django.urls import reverse
from django.contrib.auth import login as auth_login
from django.contrib.auth import views as auth_views


def index(request):
    return render(request, "cabinet/index.html", locals())


def login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("cabinet_sites_index"))
    return auth_views.login(request, template_name="cabinet/login.html")


RegistrationForm = modelform_factory(User, fields=["username", "email", "password"])


def registration(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("cabinet_sites_index"))

    form = RegistrationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = User.objects.create_user(form.cleaned_data["username"], form.cleaned_data["email"], form.cleaned_data["password"])
        auth_login(request, user)
        messages.success(request, "Вы успешно зарегистрировались")
        return HttpResponseRedirect(reverse("cabinet_sites_index"))

    return render(request, "cabinet/registration.html", locals())
