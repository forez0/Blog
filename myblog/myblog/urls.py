"""
Основний файл маршрутизації для проєкту MyBlog.

Цей файл містить основні шляхи, включаючи доступ до адміністративної панелі та шляхи блогу.

:urls:
    /admin/        — адміністративна панель Django (admin.site.urls)
    /              — домашня сторінка, перенаправлення до блогу (blog.urls)
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
]
