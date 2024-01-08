from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from api.views import (
    FileUploadView,
    UserFileDetailUpdateDeleteView,
    UserFilesListView,
    VideoCropProgressView,
    VideoCropView,
)

from django.urls import path

urlpatterns = [
    path("token/", TokenObtainPairView.as_view()),
    path("token/refresh/", TokenRefreshView.as_view()),
    # File upload
    path("files/", UserFilesListView.as_view()),
    path("files/<int:pk>/", UserFileDetailUpdateDeleteView.as_view()),
    path("file-upload/", FileUploadView.as_view()),
    # Crop video
    path("video-crop/", VideoCropView.as_view()),
    # Check cropping video status
    path(
        "video-status/<int:pk>/", VideoCropProgressView.as_view(), name="video-status"
    ),
]
