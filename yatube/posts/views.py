from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from core.utils import paginate
from posts.forms import CommentForm, PostForm
from posts.models import Comment, Group, Post

User = get_user_model()


def index(request: HttpRequest) -> HttpResponse:
    posts = Post.objects.select_related(
        'author',
        'group',
    )
    return render(
        request,
        'posts/index.html',
        {
            'page_obj': paginate(request, posts),
        },
    )


def group_posts(request: HttpRequest, slug: str) -> HttpResponse:
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.select_related(
        'author',
        'group',
    )
    return render(
        request,
        'posts/group_list.html',
        {
            'page_obj': paginate(request, posts),
            'group': group,
        },
    )


def profile(request: HttpRequest, username: str) -> HttpResponse:
    user = get_object_or_404(User, username=username)
    posts = user.posts.select_related(
        'author',
    )
    return render(
        request,
        'posts/profile.html',
        {
            'page_obj': paginate(request, posts),
            'author': user,
        },
    )


def post_detail(request: HttpRequest, pk: int) -> HttpResponse:
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.select_related(
        'author',
    )
    form = CommentForm(
        request.POST or None,
    )
    return render(
        request,
        'posts/post_detail.html',
        {
            'post': post,
            'comments': comments,
            'form': form,
        },
    )


@login_required
def post_create(request: HttpRequest) -> HttpResponse:
    form = PostForm(
        request.POST or None,
        files=request.FILES or None,
    )
    if not form.is_valid():
        return render(
            request,
            'posts/create_post.html',
            {
                'form': form,
            },
        )
    form.instance.author = request.user
    form.save()
    return redirect('posts:profile', request.user.username)


@login_required
def post_edit(request: HttpRequest, pk: int) -> HttpResponse:
    post = get_object_or_404(Post, id=pk)
    if request.user != post.author:
        return redirect('posts:post_detail', pk)
    form = PostForm(
        request.POST or None,
        files=request.FILES or None,
        instance=post,
    )
    if not form.is_valid():
        return render(
            request,
            'posts/create_post.html',
            {
                'is_edit': True,
                'form': form,
            },
        )
    post.save()
    return redirect('posts:post_detail', pk)


@login_required
def add_comment(request: HttpRequest, post_id: int) -> HttpResponse:
    form = CommentForm(request.POST)
    post = get_object_or_404(Post, pk=post_id)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('posts:post_detail', pk=post_id)
