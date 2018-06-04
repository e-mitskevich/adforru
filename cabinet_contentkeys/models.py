from django.db import models

# Create your models here.
from django.db.models import CASCADE

from cabinet_sites.models import Site


class ContentKey(models.Model):
    site = models.ForeignKey(Site, verbose_name="Сайт", related_name="contentkeys", null=False, on_delete=CASCADE)
    param_value = models.CharField("Значение", max_length=500, null=False)
    unique_users = models.PositiveIntegerField(default=0)
    pageviews = models.PositiveIntegerField(default=0)
    conversions = models.PositiveIntegerField(default=0)

    def cvr(self):
        if self.conversions > 0:
            return round(float(self.conversions) / self.unique_users * 100, 2)
        return 0
