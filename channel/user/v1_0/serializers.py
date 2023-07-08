from rest_framework import serializers

from channel.models import Channel


class ChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = [
            "url",
            "title",
            "thumbnail",
            "outputFolder",
        ]


class SearchChannelSerializer(serializers.Serializer):
    url = serializers.CharField()


class ImportTrackingSerialzier(serializers.Serializer):
    file = serializers.FileField()
