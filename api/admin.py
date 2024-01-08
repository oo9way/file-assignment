from django.contrib import admin
from api.models import UserFile, VideoCropProgress


admin.site.register([UserFile, VideoCropProgress])
