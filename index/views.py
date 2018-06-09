import json
import uuid

from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from index.models import TrackerLogEntry


def home(request):
    return render(request, "index/home.html", locals())


COOKIE_NAME = "firsttds_mark"


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
        cookie_mark=request.COOKIES.get(COOKIE_NAME, "")
    ).save()

    response = HttpResponseRedirect(redirect_to)
    mark = request.COOKIES.get(COOKIE_NAME, str(uuid.uuid1()))
    response.set_cookie(COOKIE_NAME, mark, domain=request.META.get("HTTP_HOST", "").split(":")[0])
    return response
