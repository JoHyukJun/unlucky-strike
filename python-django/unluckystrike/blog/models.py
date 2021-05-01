from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

import urllib
from ckeditor.fields import RichTextField


# Create your models here.

STATUS = (
    (0, 'Draft'),
    (1, 'Publish')
)

class Category(models.Model):
    name = models.CharField(max_length=20)
    created_on = models.DateTimeField(auto_now_add=True, null=True)
    last_modified = models.DateTimeField(auto_now=True, null=True)
    
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('blog_category', args=[str(self.name)])


class Post(models.Model):
    title = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_list')
    body = RichTextField(blank=True, null=True)
    upload_file = models.FileField(blank=True, null=True, upload_to='blog/')
    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    categories = models.ManyToManyField('Category', blank=True, related_name='posts')
    status = models.IntegerField(choices=STATUS, default=1)

    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        return self.title + ' | ' + str(self.author)

    def get_absolute_url(self):
        return reverse('blog_detail', args=[str(self.id), str(self.title)])
    


class Comment(models.Model):
    author = models.CharField(max_length=60)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)

    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        return "Comment {} by {}".format(self.body, self.author)
