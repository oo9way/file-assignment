from django.db import models
from django.contrib.auth.models import User


class UserFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to="uploads/")
    info = models.JSONField(null=True, blank=True)


class VideoCropProgress(models.Model):
    STATUS = (
        ("process", "In progress"),
        ("completed", "Completed"),
        ("failed", "Failed"),
    )

    video = models.ForeignKey(UserFile, on_delete=models.CASCADE)
    start_time = models.IntegerField(default=0)
    end_time = models.IntegerField(default=0)

    status = models.CharField(max_length=16, choices=STATUS, default="process")
