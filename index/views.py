import json
import uuid
from urllib.parse import urlparse, parse_qs

import requests
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.utils.http import urlencode

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


def ebay(request):
    get_params = {
        'SECURITY-APPNAME': 'EvgenijM-Testappl-PRD-62ccbdeee-ae1b5bd7',
        'OPERATION-NAME': 'findItemsByKeywords',
        'SERVICE-VERSION': '1.0.0',
        'RESPONSE-DATA-FORMAT': 'JSON',
        'callback': '_cb_findItemsByKeywords',
        'keywords': 'iPhone 7 plus 32gb unlocked black',
        'paginationInput.entriesPerPage': '100',
        'sortOrder': 'PricePlusShippingLowest',
        'GLOBAL-ID': 'EBAY-US',
        'siteid': '0'
    }

    url = "https://svcs.ebay.com/services/search/FindingService/v1?" + urlencode(get_params)
    result = requests.get(url).text

    return render(request, "index/ebay.html", locals())


def telegram(request):
    pass