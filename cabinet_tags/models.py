from django.db import models

# Create your models here.
from django.db.models import CASCADE

from cabinet_contentkeys.models import ContentKey
from cabinet_sites.models import Site


class Tag(models.Model):
    site = models.ForeignKey(Site, verbose_name="Сайт", related_name="tags", on_delete=CASCADE, null=False)
    title = models.CharField("Название", max_length=500, null=False)
    selector = models.CharField("Селектор", max_length=500, null=False)
    created = models.DateTimeField(auto_now_add=True, null=False)


class TagValue(models.Model):
    tag = models.ForeignKey(Tag, verbose_name="Блок", related_name="tag_values", on_delete=CASCADE, null=False)
    contentkey = models.ForeignKey(ContentKey, verbose_name="Контент-ключ", related_name="tag_values", on_delete=CASCADE, null=False)
    value = models.TextField("Содержимое", null=False, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=False)
    updated = models.DateTimeField(auto_now=True, null=False)
