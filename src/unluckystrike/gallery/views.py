from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.urls import reverse
from django.utils import timezone
from django import forms
from django.db import transaction

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Gallery, Photo, Tag, Comment, Post
from .forms import PostForm


@login_required
@transaction.atomic
def photo_upload(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.uploaded_by = request.user
            post.save()
            
            # 태그 처리
            tags_text = form.cleaned_data.get("tags_text", "")
            if tags_text:
                tag_names = [t.strip() for t in tags_text.split(",") if t.strip()]
                for name in tag_names:
                    tag, _ = Tag.objects.get_or_create(name=name)
                    post.tags.add(tag)
            
            # 여러 이미지 처리
            images = form.cleaned_data.get('images', [])
            for idx, image in enumerate(images):
                Photo.objects.create(
                    post=post,
                    image=image,
                    order=idx
                )
            
            return redirect(reverse("gallery:post_detail", args=[post.pk]))
        return render(request, "photo_upload.html", {"form": form})
    else:
        form = PostForm()
    return render(request, "photo_upload.html", {"form": form})

def gallery_index(request):
    qs = Post.objects.filter(is_public=True).select_related("uploaded_by").prefetch_related("photos", "tags")
    paginator = Paginator(qs, 18)
    page = request.GET.get("page", 1)
    posts = paginator.get_page(page)
    context = {"posts": posts}
    return render(request, "gallery_index.html", context)


def gallery_detail(request, slug):
    """
    앨범(컬렉션) 상세: 해당 갤러리에 속한 사진 목록
    """
    gallery = get_object_or_404(Gallery, slug=slug)
    qs = gallery.photos.filter(is_public=True).prefetch_related("tags")
    paginator = Paginator(qs, 18)
    page = request.GET.get("page", 1)
    photos = paginator.get_page(page)
    return render(request, "gallery_detail.html", {"gallery": gallery, "photos": photos})


def photo_detail(request, pk):
    """
    사진 상세(모달/페이지용). AJAX 요청이면 JSON, 일반 요청이면 템플릿 렌더링
    """
    photo = get_object_or_404(Photo, pk=pk)
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        data = {
            "id": photo.pk,
            "src": photo.image.url,
            "caption": photo.caption,
            "taken_date": photo.taken_date.isoformat() if photo.taken_date else None,
            "uploaded_by": getattr(photo.uploaded_by, "username", None),
            "likes_count": photo.likes.count(),
            "tags": [t.name for t in photo.tags.all()],
        }
        return JsonResponse(data)
    # non-AJAX: render detail page
    comments = photo.comments.filter(is_removed=False).select_related("user")
    return render(request, "photo_detail.html", {"photo": photo, "comments": comments})


@login_required
def photo_like(request, pk):
    """
    좋아요 토글. POST 요청만 허용.
    반환: JSON {status: 'liked'|'unliked', likes_count: N}
    """
    if request.method != "POST":
        return HttpResponseBadRequest("POST required")
    photo = get_object_or_404(Photo, pk=pk)
    user = request.user
    if user in photo.likes.all():
        photo.likes.remove(user)
        status_text = "unliked"
    else:
        photo.likes.add(user)
        status_text = "liked"
    return JsonResponse({"status": status_text, "likes_count": photo.likes.count()})


def tagged_photos(request, name):
    """
    태그별 사진 목록
    """
    tag = get_object_or_404(Tag, name=name)
    qs = tag.photos.filter(is_public=True).prefetch_related("tags")
    paginator = Paginator(qs, 18)
    page = request.GET.get("page", 1)
    photos = paginator.get_page(page)
    return render(request, "tagged_photos.html", {"tag": tag, "photos": photos})


class PhotoListAPI(APIView):
    """
    간단한 API: GET -> 공개 사진 리스트 반환 (최신 순)
    """
    def get(self, request, format=None):
        qs = Photo.objects.filter(is_public=True).order_by("-created_at")[:200]
        data = []
        for p in qs:
            data.append({
                "id": p.pk,
                "src": request.build_absolute_uri(p.image.url),
                "caption": p.caption,
                "taken_date": p.taken_date.isoformat() if p.taken_date else None,
                "uploaded_by": getattr(p.uploaded_by, "username", None),
                "likes_count": p.likes.count(),
                "tags": [t.name for t in p.tags.all()],
            })
        return Response(data, status=status.HTTP_200_OK)

def post_detail(request, pk):
    """
    포스트 상세(모달/페이지용). AJAX 요청이면 JSON
    """
    post = get_object_or_404(Post, pk=pk)
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        photos = [{"src": p.image.url, "taken_date": p.taken_date.isoformat() if p.taken_date else None} 
                  for p in post.photos.all()]
        data = {
            "id": post.pk,
            "photos": photos,
            "caption": post.caption,
            "uploaded_by": getattr(post.uploaded_by, "username", None),
            "likes_count": post.likes.count(),
            "tags": [t.name for t in post.tags.all()],
        }
        return JsonResponse(data)
    # non-AJAX: render detail page
    comments = post.comments.filter(is_removed=False).select_related("user")
    return render(request, "gallery/post_detail.html", {"post": post, "comments": comments})

@login_required
def post_like(request, pk):
    """
    좋아요 토글 (Post 기반)
    """
    if request.method != "POST":
        return HttpResponseBadRequest("POST required")
    post = get_object_or_404(Post, pk=pk)
    user = request.user
    if user in post.likes.all():
        post.likes.remove(user)
        status_text = "unliked"
    else:
        post.likes.add(user)
        status_text = "liked"
    return JsonResponse({"status": status_text, "likes_count": post.likes.count()})