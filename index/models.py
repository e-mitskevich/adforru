from django.db import models

# Create your models here.


class TrackerLogEntry(models.Model):
    time = models.DateTimeField(auto_now=True)
    request_get = models.TextField()
    request_post = models.TextField()
    request_files = models.TextField()
    request_cookies = models.TextField()
    request_meta = models.TextField()

    ip = models.CharField(max_length=32, default="")
    useragent = models.CharField(max_length=500, default="")
    cookie_mark = models.CharField(max_length=64, default="")
