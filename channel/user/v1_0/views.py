from django.shortcuts import render
from rest_framework.generics import CreateAPIView, ListCreateAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from channel.models import Channel
from channel.tasks import run_tracking_check
from .serializers import (
    ChannelSerializer,
    ImportTrackingSerialzier,
    SearchChannelSerializer,
)


class SearchAPIView(ListCreateAPIView):
    permission_classes = ()
    serializer_class = SearchChannelSerializer
    queryset = Channel.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            url = data["url"]
            channels = Channel.objects.filter(url__icontains=url)
            if channels:
                """
                nếu có channel
                trả về danh sách channel
                """
                serializer = ChannelSerializer(instance=channels, many=True)
                data = dict(results=serializer.data, keyword=url)
                render(request, "channel/search.html", data)
            else:
                new_channel = Channel.objects.create(url=url)
                serializer = ChannelSerializer(instance=new_channel)
                data = dict(
                    results=[
                        serializer.data,
                    ],
                    keyword=url,
                )
            return render(request, "channel/search_result.html", data)

    def get(self, request, *args, **kwargs):
        return render(request, "channel/search.html")


class ImportAPIView(ListCreateAPIView):
    permission_classes = ()
    serializer_class = ImportTrackingSerialzier
    queryset = Channel.objects.all()

    def post(self, request, *args, **kwargs):
        files = request.FILES
        for file in files:
            print(file)
            print(files.get(file))
            '''
            Lưu tệp lại rồi sau đó truyền vị trí tệp vào trong celery task
            '''
            filename=None
            run_tracking_check.delay(filename=filename)
        """
        get the upload files here and parse it
        """
        return Response(data=dict(message="success"))

    def get(self, request, *args, **kwargs):
        return render(request, "channel/import_file.html")
