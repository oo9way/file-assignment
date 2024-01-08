from rest_framework import serializers
from api.models import UserFile, VideoCropProgress


class FileModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFile
        fields = ("file", "info")


class VideoCropProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoCropProgress
        fields = ("status",)
