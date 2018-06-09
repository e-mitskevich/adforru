import json
import uuid

from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from index.models import TrackerLogEntry


def home(request):
    return render(request, "index/home.html", locals())


def tracker(request):
    redirect_to = request.GET["lp"]

    TrackerLogEntry(
        request_url=request.build_absolute_uri(),
        request_get=json.dumps(request.GET),
        request_post=json.dumps(request.POST),
        request_files=json.dumps(request.FILES),
        request_cookies=request.COOKIES,
        request_meta=request.META,

        ip=request.META.get("REMOTE_ADDR", ""),
        useragent=request.META.get("HTTP_USER_AGENT", ""),
        cookie_mark=request.COOKIES.get("firsttds_mark", "")
    ).save()

    response = HttpResponseRedirect(redirect_to)
    response.set_cookie("firsttds_mark", str(uuid.uuid1()))
    return response
