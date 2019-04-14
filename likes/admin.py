from django.contrib import admin
from .models import LikeRecord, LikeCount

# Register your models here.

@admin.register(LikeRecord)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('content_object', 'user', 'like_time')

    def content_object(self, obj):
        return obj.content_object