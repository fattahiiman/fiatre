from django.contrib import admin
from .models import *

@admin.register(Episode)
class EpisodeAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'time', 'episode', 'description', 'category',
                    'image' , 'video' , 'type' , 'created_at', 'updated_at']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(EpisodeDownload)
class EpisodeDownloadAdmin(admin.ModelAdmin):
    list_display = ['user', 'episode' , 'created_at', 'updated_at']
    readonly_fields = ['created_at', 'updated_at']
