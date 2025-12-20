from django.db import models
from django.conf import settings
from django.utils import timezone
import os
from uuid import uuid4

def photo_upload_to(instance, filename):
    ext = os.path.splitext(filename)[1].lower()
    # 파일명 충돌 방지: UUID + 원래 확장자, 연/월 디렉터리
    return f'gallery/{timezone.now().strftime("%Y/%m")}/{uuid4().hex}{ext}'

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

class Gallery(models.Model):
    title = models.CharField(max_length=150)
    slug = models.SlugField(max_length=160, unique=True)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

class Post(models.Model):
    """
    여러 사진을 묶는 포스트
    """
    gallery = models.ForeignKey(Gallery, null=True, blank=True, on_delete=models.SET_NULL, related_name='posts')
    caption = models.TextField(blank=True)
    tags = models.ManyToManyField(Tag, blank=True, related_name='posts')
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name='posts')
    is_public = models.BooleanField(default=True)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='liked_posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Post #{self.pk} by {self.uploaded_by or "anonymous"}'

    def thumbnail(self):
        """첫 번째 사진을 썸네일로 사용"""
        return self.photos.first()

class Photo(models.Model):
    """
    각 사진 레코드 (Post에 종속)
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to=photo_upload_to)
    order = models.PositiveIntegerField(default=0)  # 사진 순서
    taken_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'created_at']

    def __str__(self):
        return f'Photo #{self.pk} in Post #{self.post_id}'

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_removed = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'Comment #{self.pk} on Post #{self.post_id}'