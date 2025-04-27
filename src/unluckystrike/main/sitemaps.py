#-*- coding: utf-8 -*-

from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from blog.models import Post, Category


class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return [
            'home_index',
            'home_about',
            'home_contact',
            'project_index',
            'blog_index',
        ]

    def location(self, item):
        return reverse(item)


class PostSiteMap(Sitemap):
    priority = 0.6
    changefreq = 'weekly'

    def items(self):
        return Post.objects.all().filter(status=1).order_by('-created_on')

    def lastmod(self, obj):
        return obj.last_modified


class CategorySiteMap(Sitemap):
    priority = 0.6
    changefreq = 'weekly'

    def items(self):
        return Category.objects.all()

    def lastmod(self, obj):
        return obj.last_modified