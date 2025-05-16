from django.contrib import admin
from .models import TextContent, ImageContent, VideoContent, FileContent

admin.site.register(FileContent)
admin.site.register(TextContent)
admin.site.register(ImageContent)
admin.site.register(VideoContent)