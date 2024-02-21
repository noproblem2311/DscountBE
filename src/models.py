from django.db import models
from django.contrib.auth.models import User

class VideoTranscription(models.Model):
    video_url = models.URLField(max_length=1024, verbose_name="Video URL")
    transcript = models.TextField(verbose_name="Transcription", blank=True, null=True)
    upload_time = models.DateTimeField(auto_now_add=True, verbose_name="Upload Time")
    transcription_time = models.DateTimeField(blank=True, null=True, verbose_name="Transcription Completed Time")
    note = models.TextField(verbose_name="Note", blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='video_transcriptions')
    
    def __str__(self):
        return f"Video uploaded on {self.upload_time.strftime('%Y-%m-%d %H:%M:%S')}"