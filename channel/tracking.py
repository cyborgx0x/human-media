import xml.etree.ElementTree as ET

from channel.models import Channel, Video


def tracking():
    filename = "C:/Users/Luke/Downloads/tracking.mhx"
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

        new_channel = Channel.objects.create(
            url=channel_url,
            title=title,
            thumbnail=thumbnail,
            lastUpdate=lastUpdate,
            outputFolder=outputFolder,
        )
        try:
            new_channel.save()
            
        except Exception as e:
            print(e)
        channel_id = new_channel.id
        print(channel_id)
        videos = channel.findall("./videos/v")
        print(len(videos))
        for video in videos:
            video_id = video.get("id")
            new_video = Video.objects.create(video_id=video_id, channel_id=channel_id)
            try:
                new_video.save()

            except Exception as e:
                print(e)


tracking()
