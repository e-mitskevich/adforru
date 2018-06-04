from django.contrib import messages
from django.forms import modelform_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.urls import reverse

from cabinet_sites.models import Site
from cabinet_tags.models import Tag


TagEditForm = modelform_factory(Tag, fields=["site", "title", "selector"])


def edit(request, site_id, tag_id=None):
    site_id = int(site_id)

    site = get_object_or_404(Site, user=request.user, pk=site_id)

    if tag_id is not None:
        tag_id = int(tag_id)
        tag = get_object_or_404(Tag, site_id=site_id, pk=tag_id)
    else:
        tag = Tag(site_id=site_id)

    form = TagEditForm(request.POST or None, instance=tag)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Сохранено")
        return HttpResponseRedirect(reverse("cabinet_sites_show", args=[site_id]))
    return render(request, "cabinet_tags/edit.html", locals())


def delete(request, site_id, tag_id):
    site_id = int(site_id)
    tag_id = int(tag_id)

    site = get_object_or_404(Site, user=request.user, pk=site_id)
    get_object_or_404(Tag, site=site, pk=tag_id).delete()
    messages.success(request, "Удалено")
    return HttpResponseRedirect(reverse("cabinet_sites_show", args=[site_id]))