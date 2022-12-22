from django.core import paginator
from django.shortcuts import get_object_or_404, render
from django.views import generic
#from rest_framework import generics
from django.db.models import Q
from django.views.generic import View, ListView, DetailView, FormView, CreateView
from django.contrib import messages

from blog.models import Category, Post, Comment
from blog.forms import CommentForm

import random


# Create your views here.


class BlogListView(ListView):
    model = Post
    paginate_by = 5
    template_name = 'blog_index.html'
    context_object_name = 'post_list'


    def get_queryset(self):
        search_keyword = self.request.GET.get('q', '')
        search_type = self.request.GET.get('type', '')
        post_list = Post.objects.filter(status=1).order_by('-created_on')

        if search_keyword:
            if len(search_keyword) > 1:
                try:
                    if search_type == 'all':
                        search_post_list = post_list.filter(Q (title__icontains=search_keyword) | Q(body__icontains=search_keyword))
                    elif search_type == 'title':
                        search_post_list = post_list.filter(title__icontains=search_keyword)
                    elif search_type == 'content':
                        search_post_list = post_list.filter(body__icontains=search_keyword)

                    return search_post_list
                except:
                    messages.error(self.request, 'No results were found for your search')
            else:
                messages.error(self.request, '')
        
        return post_list


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Adding pagination using function based views.
        paginator = context['paginator']
        page_numbers_range = 5
        max_idx = len(paginator.page_range)

        page = self.request.GET.get('page')
        cur_page = int(page) if page else 1

        start_idx = int((cur_page - 1) / page_numbers_range) * page_numbers_range
        end_idx = start_idx + page_numbers_range
        if end_idx >= max_idx:
            end_idx = max_idx

        page_range = paginator.page_range[start_idx:end_idx]
        context['page_range'] = page_range

        search_keyword = self.request.GET.get('q', '')
        search_type = self.request.GET.get('type', '')

        if len(search_keyword) > 1 :
            context['q'] = search_keyword
        context['type'] = search_type

        # Adding categories data.
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(status=1, categories=None).count()

        return context


'''
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
'''


def blog_category(request, category):
    posts = Post.objects.filter(status=1,
        categories__name__contains=category
    ).order_by('-created_on')

    context = {
        "category": category,
        "posts": posts
    }

    return render(request, "blog_category.html", context)


def blog_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    form = CommentForm()
    comment_validator = (random.randint(10, 99))
    
    if request.method == 'POST':
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = Comment(
                author=form.cleaned_data["author"],
                body=form.cleaned_data["body"],
                post=post
            )

            current_comment_validator = request.POST['current_comment_validator']

            if form.cleaned_data["verification"] == current_comment_validator:
                comment.save()

    comments = Comment.objects.filter(post=post)

    context = {
        "post": post,
        "comments": comments,
        "form": form,
        "comment_validator": comment_validator
    }

    return render(request, "blog_detail.html", context)


def blog_search(request):
    posts = Post.objects.filter(status=1).order_by('-created_on')

    search_keyword = request.POST.get('q', '')

    if search_keyword:
        posts = posts.filter(title__icontains=search_keyword)

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
            "page": page,
            "post_list": post_list,
            "q": search_keyword,
        }

        return render(request, 'blog_search.html', context)
    else:
        return render(request, 'blog_search.html')
