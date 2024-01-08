from django.shortcuts import get_object_or_404
from django.urls import reverse
from rest_framework import generics, permissions, views, response, status


from api.models import UserFile, VideoCropProgress
from api.serializers import FileModelSerializer, VideoCropProgressSerializer
from api.tasks import crop_video


class FileUploadView(generics.CreateAPIView):
    model = UserFile
    serializer_class = FileModelSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self, request):
        queryset = super().get_queryset()
        queryset = queryset.filter(user=request.user)
        return queryset

    def perform_create(self, serializer):
        instance = serializer.save(user=self.request.user)
        file = instance.file

        file_info = {
            "name": file.name.replace("uploads/", ""),
            "file_type": file.name.split(".")[-1],
            "size": file.size,
        }

        instance.info = file_info
        instance.save()


class UserFilesListView(generics.ListAPIView):
    model = UserFile
    serializer_class = FileModelSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self, request):
        queryset = super().get_queryset()
        queryset = queryset.filter(user=request.user)
        return queryset


class UserFileDetailUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    model = UserFile
    serializer_class = FileModelSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self, request):
        queryset = super().get_queryset()
        queryset = queryset.filter(user=request.user)
        return queryset


class VideoCropView(views.APIView):
    def post(self, request, *args, **kwargs):
        video_id = self.request.POST.get("video_id", None)
        start_time = self.request.POST.get("start_time", None)
        end_time = self.request.POST.get("end_time", None)

        video = get_object_or_404(UserFile, id=video_id)

        if start_time and end_time:
            progress = VideoCropProgress.objects.create(
                video=video, start_time=start_time, end_time=end_time
            )

            progress_url = reverse("video-status", args=(progress.pk,))

            crop_video.delay(video.pk, progress.pk, start_time, end_time)

            return response.Response(
                {"message": "Video cropping in progress", "status_url": progress_url},
                status=status.HTTP_202_ACCEPTED,
            )
        else:
            return response.Response(
                {"message": "Something went wrong"}, status=status.HTTP_400_BAD_REQUEST
            )


class VideoCropProgressView(generics.RetrieveAPIView):
    serializer_class = VideoCropProgressSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = VideoCropProgress.objects.all()
