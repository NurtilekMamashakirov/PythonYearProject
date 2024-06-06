from rest_framework import serializers

from .models import Chat, Link


class ChatSerializer(serializers.Serializer):
    id = serializers.IntegerField()


class LinkSerializer(serializers.Serializer):
    url = serializers.CharField()
    updated_at = serializers.DateTimeField(read_only=True)
    checked_at = serializers.DateTimeField(read_only=True)
