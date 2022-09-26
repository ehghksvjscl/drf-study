from django.contrib import admin

# Register your models here.
from django.contrib import admin
from medias.models import Photo, Video


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    pass


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    pass
