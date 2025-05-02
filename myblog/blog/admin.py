"""Адміністративна конфігурація для моделі Post та Comment додатку blog."""
from django.contrib import admin
from .models import Post, Comment

admin.site.register(Post)
admin.site.register(Comment)
