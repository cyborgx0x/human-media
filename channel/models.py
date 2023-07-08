from django.db import models


# Create your models here.
class Channel(models.Model):
    url = models.CharField(max_length=250)
    title = models.CharField(max_length=250, null=True, blank=True)
    thumbnail = models.CharField(max_length=250, null=True, blank=True)
    outputFolder = models.TextField()
