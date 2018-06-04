from urllib.parse import urlparse, parse_qs

from django import forms
from django.contrib import messages
from django.db.models import Prefetch
from django.forms import modelform_factory
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.urls import reverse

from cabinet_contentkeys.models import ContentKey
from cabinet_sites.models import Site
from cabinet_tags.models import TagValue, Tag


CONTENTKEY_GET_PARAM = "content-key"


def index(request):
    sites = Site.objects.filter(user=request.user)
    return render(request, "cabinet_sites/index.html", locals())


TagValueEditForm = modelform_factory(TagValue, fields=["value"], widgets={"value": forms.Textarea(attrs={"style": "width: 100%"})})


def show(request, site_id):
    site_id = int(site_id)

    site = get_object_or_404(Site, user=request.user, pk=site_id)
    contentkeys = site.contentkeys.all()

    if CONTENTKEY_GET_PARAM not in request.GET and contentkeys.exists():
        return HttpResponseRedirect(reverse("cabinet_sites_show", args=[site.id]) + "?" + CONTENTKEY_GET_PARAM + "=" + contentkeys.first().param_value)

    tags = site.tags.all()

    selected_contentkey = ContentKey.objects.filter(param_value=request.GET.get(CONTENTKEY_GET_PARAM, None))
    if selected_contentkey.exists():
        selected_contentkey = selected_contentkey.first()
        tags = tags.prefetch_related(Prefetch("tag_values", queryset=TagValue.objects.filter(contentkey=selected_contentkey)))

    for tag in tags:
        tag.form = TagValueEditForm(request.POST or None, instance=tag.tag_values.first(), prefix=tag.id)

    if request.method == "POST":
        for tag in tags:
            if tag.form.is_valid():
                tag_value = tag.form.save(commit=False)
                tag_value.tag = tag
                tag_value.contentkey = selected_contentkey
                tag_value.save()
        messages.success(request, "Сохранено")

    contentkey_get_param = CONTENTKEY_GET_PARAM
    return render(request, "cabinet_sites/show.html", locals())


SiteEditForm = modelform_factory(Site, fields=["title", "page_url"])


def edit(request, site_id=None):
    if site_id is not None:
        site_id = int(site_id)
        site = get_object_or_404(Site, user=request.user, pk=site_id)
    else:
        site = Site(user=request.user)

    form = SiteEditForm(request.POST or None, instance=site)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Сохранено")
        return HttpResponseRedirect(reverse("cabinet_sites_index"))
    return render(request, "cabinet_sites/edit.html", locals())


def delete(request, site_id):
    site_id = int(site_id)

    get_object_or_404(Site, user=request.user, pk=site_id).delete()
    messages.success(request, "Удалено")
    return HttpResponseRedirect(reverse("cabinet_sites_index"))


COOKIE_NAME = "content_key"


def hypercontent_js(request, site_id):
    site_id = int(site_id)

    parsed = urlparse(request.META["HTTP_REFERER"])
    contentkey_str_current = parse_qs(parsed.query).get(CONTENTKEY_GET_PARAM, [None])[0]

    contentkey_str_used = contentkey_str_current
    contentkey = ContentKey.objects.filter(site_id=site_id, param_value=contentkey_str_used)
    if not contentkey.exists() and COOKIE_NAME in request.COOKIES:
        contentkey_str_used = request.COOKIES[COOKIE_NAME]
        contentkey = ContentKey.objects.filter(site_id=site_id, param_value=contentkey_str_used)
    if not contentkey.exists():
        response = HttpResponse()
        _set_js_content_type(response)
        return response
    contentkey = contentkey.first()

    contentkey.pageviews += 1
    if COOKIE_NAME not in request.COOKIES or request.COOKIES[COOKIE_NAME] != contentkey_str_used:
        contentkey.unique_users += 1
    contentkey.save()

    tags = Tag.objects.filter(site_id=site_id).prefetch_related(
        Prefetch("tag_values", queryset=TagValue.objects.filter(contentkey=contentkey))
    )

    response = render(request, "cabinet_sites/hypercontent.html", locals())
    response.set_cookie(COOKIE_NAME, contentkey.param_value, max_age=3600 * 24 * 7, path="/")
    _set_js_content_type(response)
    return response


def conversion_js(request, site_id):
    site_id = int(site_id)

    contentkey_str_used = request.COOKIES.get(COOKIE_NAME, None)
    contentkey = ContentKey.objects.filter(site_id=site_id, param_value=contentkey_str_used)

    if not contentkey.exists():
        response = HttpResponse()
        _set_js_content_type(response)
        return response

    contentkey = contentkey.first()
    contentkey.conversions += 1
    contentkey.save()

    response = HttpResponse()
    response.set_cookie(COOKIE_NAME, contentkey.param_value, max_age=3600 * 24 * 7, path="/")
    _set_js_content_type(response)
    return response


def _set_js_content_type(response):
    response["Content-type"] = "application/x-javascript"
