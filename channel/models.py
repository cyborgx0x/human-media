from django.db import models


# Create your models here.
class Channel(models.Model):
    id = models.AutoField(primary_key=True)
    url = models.CharField(max_length=250)
    title = models.CharField(max_length=250, null=True, blank=True)
    thumbnail = models.CharField(max_length=250, null=True, blank=True)
    outputFolder = models.TextField(null=True)
    '''
    check trùng channel_id
    '''
    channel_id = models.CharField(max_length=250, null=True)
    lastUpdate = models.DateTimeField(null=True)
    
class Video(models.Model):
    video_id = models.CharField(max_length=250, unique=True)
    channel = models.ForeignKey(Channel, related_name="video", on_delete=models.CASCADE, null=True, unique=True)
