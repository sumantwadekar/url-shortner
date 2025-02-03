from rest_framework import serializers


class URLSerializer(serializers.Serializer):
    long_url = serializers.URLField(required=True)
