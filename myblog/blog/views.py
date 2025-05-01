"""Представлення для блогу — обробляє реєстрацію користувачів,
 автентифікацію та керування дописами."""

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect

from .forms import PostForm, CommentForm, RegistrationForm
from .models import Post


def register(request):
    """Обробка реєстрації нового користувача.

    Аргументи:
        request: об'єкт HttpRequest

    Повертає:
        HttpResponse: сторінка реєстрації або перенаправлення на вхід
    """
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, 'Реєстрація успішна! Тепер ви можете увійти.')
            return redirect('login')
        messages.error(request, 'Помилка при реєстрації. Перевірте введені дані.')
    form = RegistrationForm()
    return render(request, 'blog/register.html', {'form': form})


def login_view(request):
    """Обробка входу користувача.

    Аргументи:
        request: об'єкт HttpRequest

    Повертає:
        HttpResponse: сторінка входу або перенаправлення до списку дописів
    """
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Успішний вхід!')
            return redirect('post_list')
        messages.error(request, 'Невірне ім\'я користувача або пароль.')
    form = AuthenticationForm()
    return render(request, 'blog/login.html', {'form': form})


def post_list(request):
    """Відображення списку дописів з пагінацією та пошуком.

    Аргументи:
        request: об'єкт HttpRequest

    Повертає:
        HttpResponse: сторінка зі списком дописів
    """
    query = request.GET.get('q')
    posts_list = Post.objects.filter(  # pylint: disable=no-member
        Q(title__icontains=query) | Q(content__icontains=query)
    ).order_by('-created_at') if query else Post.objects.all().order_by('-created_at')  # pylint: disable=no-member

    paginator = Paginator(posts_list, 5)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)
    return render(request, 'blog/post_list.html', {'posts': posts})


def logout_view(request):
    """Обробка виходу користувача.

    Аргументи:
        request: об'єкт HttpRequest

    Повертає:
        HttpResponseRedirect: перенаправлення на сторінку входу
    """
    logout(request)
    return redirect('login')


def post_detail(request, pk):
    """Відображення деталей допису та обробка додавання коментаря.

    Аргументи:
        request: об'єкт HttpRequest
        pk: первинний ключ допису

    Повертає:
        HttpResponse: сторінка деталей допису
    """
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    form = CommentForm()
    return render(request, 'blog/post_detail.html', {'post': post, 'form': form})


def add_comment(request, pk):
    """Додавання коментаря до допису.

    Аргументи:
        request: об'єкт HttpRequest
        pk: первинний ключ допису

    Повертає:
        HttpResponseRedirect: перенаправлення до сторінки деталей допису
    """
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST, request=request)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            if request.user.is_authenticated:
                comment.author = request.user
            comment.save()
            return redirect('post_detail', pk=post.pk)
    return redirect('post_detail', pk=post.pk)


@login_required
def post_create(request):
    """Створення нового допису в блозі.

    Аргументи:
        request: об'єкт HttpRequest

    Повертає:
        HttpResponse: форма створення допису або перенаправлення до деталей
    """
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, request=request)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    form = PostForm(request=request)
    return render(request, 'blog/post_create.html', {'form': form})


@login_required
def post_edit(request, pk):
    """Редагування наявного допису в блозі.

    Аргументи:
        request: об'єкт HttpRequest
        pk: первинний ключ допису

    Повертає:
        HttpResponse: форма редагування або перенаправлення до деталей
    """
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post, request=request)
        if form.is_valid():
            form.save()
            return redirect('post_detail', pk=post.pk)
    form = PostForm(instance=post, request=request)
    return render(request, 'blog/post_edit.html', {'form': form})


@login_required
def post_delete(request, pk):
    """Видалення допису з блогу.

    Аргументи:
        request: об'єкт HttpRequest
        pk: первинний ключ допису

    Повертає:
        HttpResponse: сторінка підтвердження або перенаправлення до списку
    """
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        post.delete()
        messages.success(request, "Пост успішно видалено")
        return redirect('post_list')
    return render(request, 'blog/post_confirm_delete.html', {'post': post})
