from django.urls import path
from . import views

app_name = "gallery"

urlpatterns = [
    path('', views.gallery_index, name='gallery_index'),                        # 그리드(피드) 화면
    path('upload/', views.photo_upload, name='photo_upload'),                    # 사진 업로드 (폼)
    path('album/<slug:slug>/', views.gallery_detail, name='gallery_detail'),     # 앨범/컬렉션 상세
    path('post/<int:pk>/', views.post_detail, name='post_detail'),            # 사진 상세(모달 등)
    path('post/<int:pk>/like/', views.post_like, name='post_like'),           # 좋아요 토글 (POST)
    path('tag/<str:name>/', views.tagged_photos, name='tagged_photos'),         # 태그별 목록
    path('api/photos/', views.PhotoListAPI.as_view(), name='api_photos'),
]