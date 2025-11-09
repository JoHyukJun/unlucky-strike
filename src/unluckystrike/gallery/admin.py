from django.contrib import admin
from .models import Gallery, Photo, Tag, Comment, Post

@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ("title", "created_by", "created_at")

class PhotoInline(admin.TabularInline):
    model = Photo
    extra = 1
    fields = ('image', 'order', 'taken_date')

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("pk", "caption_short", "uploaded_by", "is_public", "created_at")
    list_filter = ("is_public", "created_at")
    search_fields = ("caption",)
    inlines = [PhotoInline]
    
    def caption_short(self, obj):
        return obj.caption[:50] if obj.caption else "-"
    caption_short.short_description = "Caption"

@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ("pk", "post", "order", "taken_date", "created_at")
    list_filter = ("created_at",)
    search_fields = ("post__caption",)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("pk", "post", "user", "created_at", "is_removed")
    list_filter = ("is_removed", "created_at")
    search_fields = ("text", "post__caption")