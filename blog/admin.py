from django.contrib import admin
from django.utils import timezone

from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    fields = ("title", "text", "image", "published_date")
    list_display = ("title", "author", "published_date")

    def save_model(self, request, obj, form, change):
        if not obj.author_id:
            obj.author = request.user
        if not obj.published_date:
            obj.published_date = timezone.now()
        super().save_model(request, obj, form, change)
