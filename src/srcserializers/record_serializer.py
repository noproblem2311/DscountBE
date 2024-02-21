from rest_framework import serializers
from ..models import VideoTranscription

class VideoTranscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoTranscription
        fields = ['id', 'video_url', 'transcript', 'upload_time', 'transcription_time', 'note', 'user']


