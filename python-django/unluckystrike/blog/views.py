from django.shortcuts import render
from django.views import generic
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from blog.models import Post, Comment
from blog.forms import CommentForm


# Create your views here.

def blog_index(request):
    posts = Post.objects.filter(status=1).order_by('-created_on')

    # Adding pagination using function based views.
    paginator = Paginator(posts, 5)
    page = request.GET.get('page')

    try:
        post_list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page.
        post_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results.
        post_list = paginator.page(paginator.num_pages)

    context = {
        #"posts": posts,
        "page": page,
        "post_list": post_list,
    }

    return render(request, "blog_index.html", context)


def blog_category(request, category):
    posts = Post.objects.filter(
        categories__name__contains=category
    ).order_by('-created_on')

    context = {
        "category": category,
        "posts": posts
    }

    return render(request, "blog_category.html", context)


def blog_detail(request, pk):
    post = Post.objects.get(pk=pk)
    form = CommentForm()
    
    if request.method == 'POST':
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = Comment(
                author=form.cleaned_data["author"],
                body=form.cleaned_data["body"],
                post=post
            )
            comment.save()

    comments = Comment.objects.filter(post=post)

    context = {
        "post": post,
        "comments": comments,
        "form": form,
    }

    return render(request, "blog_detail.html", context)