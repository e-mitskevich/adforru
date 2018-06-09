from django.db import models

# Create your models here.


class TrackerLogEntry(models.Model):
    time = models.DateTimeField(auto_now=True)
    request_url = models.TextField(default="")
    request_get = models.TextField(default="")
    request_post = models.TextField(default="")
    request_files = models.TextField(default="")
    request_cookies = models.TextField(default="")
    request_meta = models.TextField(default="")

    ip = models.CharField(max_length=32, default="")
    useragent = models.CharField(max_length=500, default="")
    cookie_mark = models.CharField(max_length=64, default="")
