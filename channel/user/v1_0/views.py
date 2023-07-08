from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from channel.models import Channel

from .serializers import (
    ChannelSerializer,
    ImportTrackingSerialzier,
    SearchChannelSerializer,
)


class SearchAPIView(CreateAPIView):
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
                return Response(data=serializer.data)
            """
            trả về channel được tạo mới
            """
            new_channel = Channel.objects.create(url=url)
            serializer = ChannelSerializer(instance=new_channel)
            return Response(data=serializer.data)


class ImportAPIView(CreateAPIView):
    permission_classes = ()
    serializer_class = ImportTrackingSerialzier

    def post(self, request, *args, **kwargs):
        data = self
        """
        get the upload files here and parse it
        """
        return None


