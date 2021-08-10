from django.urls import path
from django.urls import include
from . import views


urlpatterns = [
    path('', views.BlogListView.as_view(), name="blog_index"),
    path('<int:pk>/', views.blog_detail, name="blog_detail"),
    path('<category>/', views.blog_category, name="blog_category"),
    path('blog_search', views.blog_search, name="blog_search"),
]