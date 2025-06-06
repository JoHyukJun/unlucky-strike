"""engineerempire URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static

from django.contrib.sitemaps.views import sitemap

from . import settings

from main.sitemaps import StaticViewSitemap, PostSiteMap, CategorySiteMap

from django.views.generic import TemplateView

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title = 'Unlucky Strike',
        default_version = '1.00.0',
        description = 'Unlucky Strike API Document',
        terms_of_service = 'https://www.google.com/policies/terms/',
        contact = openapi.Contact(email='decibel@kakao.com'),
        license = openapi.License(name='MIT'),
    ),
    public = True,
    permission_classes = [permissions.AllowAny],
)


sitemaps = {
    'blog': PostSiteMap,
    'category': CategorySiteMap,
    'static': StaticViewSitemap,
}

# admin page custom
admin.site.site_header = "UNLUCKY STRIKE"
admin.site.index_title = "MASTER MODE"
#admin.site.site_header = "?"


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('blog/', include('blog.urls')),
    path('projects/', include('projects.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='sitemap'),
    path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
    path('ads.txt', TemplateView.as_view(template_name='ads.txt', content_type='text/plain')),
    path(r'swagger(?P<format>\.json|\.yaml)', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path(r'swagger', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path(r'redoc', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc-v1'),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)