"""
Моделі для додатку блогу: Post і Comment.
"""

from typing import Optional
from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    """
    Модель, що представляє допис у блозі.
    """

    title = models.CharField(max_length=200)
    content = models.TextField()
    author: Optional[User] = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='posts'
    )
    author_name = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='posts/', blank=True, null=True)

    def __str__(self):
        """Повертає заголовок допису."""
        return str(self.title)

    def save(self, *args, **kwargs):
        if self.author and not self.author_name:
            self.author_name = self.author.username  # pylint: disable=no-member
        super().save(*args, **kwargs)


class Comment(models.Model):
    """
    Модель, що представляє коментар до допису.
    """

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    author: Optional[User] = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='comments'
    )
    author_name = models.CharField(max_length=100, blank=True)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Повертає короткий опис коментаря."""
        author_name = getattr(self.author, 'username', self.author_name)
        post_title = getattr(self.post, 'title', 'No title')
        return f"Comment by {author_name} on {post_title}"

    def save(self, *args, **kwargs):
        if self.author and not self.author_name:
            self.author_name = self.author.username  # pylint: disable=no-member
        super().save(*args, **kwargs)
