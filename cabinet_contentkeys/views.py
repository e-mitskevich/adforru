from django.contrib import messages
from django.forms import modelform_factory
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404


# Create your views here.
from django.urls import reverse

from cabinet_contentkeys.models import ContentKey
from cabinet_sites.models import Site
from cabinet_sites.views import CONTENTKEY_GET_PARAM


def index(request, site_id):
    site_id = int(site_id)

    site = get_object_or_404(Site, user=request.user, pk=site_id)
    return render(request, "cabinet_contentkeys/index.html", locals())


ContentkeyEditForm = modelform_factory(ContentKey, fields=["param_value"])


def edit(request, site_id, contentkey_id=None):
    site_id = int(site_id)

    site = get_object_or_404(Site, user=request.user, pk=site_id)

    if contentkey_id is not None:
        contentkey_id = int(contentkey_id)
        contentkey = get_object_or_404(ContentKey, site_id=site_id, pk=contentkey_id)
    else:
        contentkey = ContentKey(site_id=site_id)

    form = ContentkeyEditForm(request.POST or None, instance=contentkey)
    if request.method == "POST" and form.is_valid():
        contentkey = form.save()
        messages.success(request, "Сохранено")
        return HttpResponseRedirect(reverse("cabinet_sites_show", args=[site_id]) + "?" + CONTENTKEY_GET_PARAM + "=" + contentkey.param_value)
    return render(request, "cabinet_contentkeys/edit.html", locals())


def delete(request, site_id, contentkey_id):
    site_id = int(site_id)
    contentkey_id = int(contentkey_id)

    site = get_object_or_404(Site, user=request.user, pk=site_id)
    get_object_or_404(ContentKey, site=site, pk=contentkey_id).delete()
    messages.success(request, "Удалено")
    return HttpResponseRedirect(reverse("cabinet_sites_show", args=[site_id]))
