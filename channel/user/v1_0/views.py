from django.shortcuts import render
from pytube import YouTube
from rest_framework.generics import CreateAPIView, ListCreateAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
import requests
from channel.models import Channel
from channel.tasks import run_tracking_check
import re
from .serializers import (
    ChannelSerializer,
    ImportTrackingSerialzier,
    SearchChannelSerializer,
)


class SearchAPIView(ListCreateAPIView):
    permission_classes = ()
    serializer_class = SearchChannelSerializer
    queryset = Channel.objects.all()

    def getChannelID(self, url):
        if "@" not in url and "channel" not in url:
            try:
                youtube = YouTube(url)
                video_channel_id = youtube.channel_id
                return video_channel_id
            except Exception as e:
                return None
        else:
            html = requests.get(url).text
            regex_pattern = r'/channel/([^{}"/]+)'
            matches = re.findall(regex_pattern, html)
            if matches:
                channel_id = matches[0]
                return channel_id
            else:
                return None

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            url = data["url"]
            channel_id = self.getChannelID(url=url)
            if channel_id == None:
                return render(request, "channel/400.html")
            channels = Channel.objects.filter(channel_id=channel_id)
            if channels:
                """
                nếu có channel
                trả về danh sách channel
                """
                serializer = ChannelSerializer(instance=channels, many=True)
                data = dict(results=serializer.data, keyword=url)
                render(request, "channel/search.html", data)
            else:
                new_channel = Channel.objects.create(url=url, channel_id=channel_id)
                serializer = ChannelSerializer(instance=new_channel)
                data = dict(
                    results=[
                        serializer.data,
                    ],
                    keyword=url,
                )
            return render(request, "channel/search_result.html", data)
        else:
            return render(request, "channel/400.html")

    def get(self, request, *args, **kwargs):
        return render(request, "channel/search.html")


class ImportAPIView(ListCreateAPIView):
    permission_classes = ()
    serializer_class = ImportTrackingSerialzier
    queryset = Channel.objects.all()

    def post(self, request, *args, **kwargs):
        files = request.FILES
        for file in files:
            """
            Lưu tệp lại rồi sau đó truyền vị trí tệp vào trong celery task
            """
            filename = None
            run_tracking_check.delay(filename=filename)
        """
        get the upload files here and parse it
        """
        return Response(data=dict(message="success"))

    def get(self, request, *args, **kwargs):
        return render(request, "channel/import_file.html")
