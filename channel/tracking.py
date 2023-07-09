import re
import xml.etree.ElementTree as ET

import requests

from channel.models import Channel, Video


def get_channel_info(channel_url):
    html = requests.get(channel_url).text
    regex_pattern = r'/channel/([^{}"/]+)'
    matches = re.findall(regex_pattern, html)
    if matches:
        channel_id = matches[0]
        return channel_id
    else:
        return None


def tracking():
    filename = "tracking.mhx"
    tree = ET.parse(filename)
    root = tree.getroot()
    channels = root.findall("./item")
    for channel in channels:
        channel_url = channel.get("url")
        title = channel.find("title").text
        author = channel.find("author").text
        thumbnail = channel.find("thumbnail").text
        lastUpdate = channel.find("lastUpdate").text
        outputFolder = channel.find("params/outputFolder").text

        channel_id = get_channel_info(channel_url=channel_url)
        if channel_id == None:
            continue
        new_channel = Channel.objects.create(
            url=channel_url,
            title=title,
            thumbnail=thumbnail,
            lastUpdate=lastUpdate,
            outputFolder=outputFolder,
            channel_id = channel_id
        )
        try:
            if not Channel.objects.filter(channel_id=channel_id).exists():
                new_channel.save()
        except Exception as e:
            print(e)

        channel_id = new_channel.id
        print(channel_id)
        videos = channel.findall("./videos/v")
        print(len(videos))
        for video in videos:
            video_id = video.get("id").split(":")[1]
            if not Video.objects.filter(video_id=video_id).exists():
                new_video = Video.objects.create(
                    video_id=video_id, channel_id=channel_id
                )
                try:
                    new_video.save()

                except Exception as e:
                    print(e)
