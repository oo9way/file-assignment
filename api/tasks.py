from celery import shared_task
from moviepy.video.io.VideoFileClip import VideoFileClip
from .models import UserFile, VideoCropProgress


@shared_task
def crop_video(video_id, progress_id, start, end):
    progress = VideoCropProgress.objects.get(id=progress_id)

    try:
        video_instance = UserFile.objects.get(pk=video_id)
        video_path = video_instance.file.path

        clip = VideoFileClip(video_path).subclip(start, end)
        cropped_video_path = video_path.replace(".mp4", "_cropped.mp4")
        clip.write_videofile(cropped_video_path, codec="libx264", audio_codec="aac")

        video_instance.file.name = cropped_video_path
        video_instance.save()

        progress.status = "completed"

    except:
        progress.status = "failed"

    progress.save()

    return cropped_video_path
