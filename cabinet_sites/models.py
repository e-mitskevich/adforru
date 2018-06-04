from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.db.models import SET_NULL


class Site(models.Model):
    user = models.ForeignKey(User, related_name="sites", null=True, on_delete=SET_NULL)
    title = models.CharField("Название", max_length=500, null=False)
    page_url = models.CharField("URL страницы", max_length=500, null=False)
    created = models.DateTimeField(auto_now_add=True, null=False)

    def __unicode__(self):
        return "%s" % self.title

    def __str__(self):
        return self.__unicode__()
