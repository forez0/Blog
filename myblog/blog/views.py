from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect
from .forms import PostForm
from .forms import CommentForm


def post_list(request):
    posts_list = Post.objects.all().order_by('-created_at')  # Отримуємо всі пости
    paginator = Paginator(posts_list, 5)  # Розбиваємо на сторінки по 5 постів
    page_number = request.GET.get('page')  # Отримуємо номер сторінки з запиту
    posts = paginator.get_page(page_number)  # Отримуємо пости для поточної сторінки
    return render(request, 'blog/post_list.html', {'posts': posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/post_detail.html', {'post': post, 'form': form})

def post_list(request):
    posts_list = Post.objects.all().order_by('-created_at')
    paginator = Paginator(posts_list, 5)  # Показуємо 5 постів на сторінці
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_list(request):
    query = request.GET.get('q')
    if query:
        posts_list = Post.objects.filter(Q(title__icontains=query)).order_by('-created_at')
    else:
        posts_list = Post.objects.all().order_by('-created_at')
    paginator = Paginator(posts_list, 5)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user  # Додаємо автора
            post.save()
            return redirect('post_list')
    else:
        form = PostForm()
    return render(request, 'blog/post_create.html', {'form': form})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})


def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        post.delete()
        return redirect('post_list')
    return render(request, 'blog/post_confirm_delete.html', {'post': post})

