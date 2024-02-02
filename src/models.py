from django.db import models

class UploadedVideo(models.Model):
    file_name = models.CharField(max_length=255, unique=True)  # Unique name of the file
    upload_time = models.DateTimeField(auto_now_add=True)  # Automatically set the time when the object is created
    video_url = models.URLField()  # The secure URL to access the video

    def __str__(self):
        return self.file_name
