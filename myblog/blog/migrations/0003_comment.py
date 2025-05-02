# blog/migrations/0003_comment.py
"""Міграція для створення моделі Comment та зв'язку з Post і User."""

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    """Створює модель коментаря, пов’язану з публікацією та користувачем."""

    dependencies = [
        ('blog', '0002_post_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(
                    auto_created=True,
                    primary_key=True,
                    serialize=False,
                    verbose_name='ID'
                )),
                ('text', models.TextField(verbose_name='Текст коментаря')),
                ('created_at', models.DateTimeField(
                    auto_now_add=True,
                    verbose_name='Дата створення'
                )),
                ('author', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='comments',
                    to=settings.AUTH_USER_MODEL,
                    verbose_name='Автор'
                )),
                ('post', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='comments',
                    to='blog.post',
                    verbose_name='Публікація'
                )),
            ],
        ),
    ]
