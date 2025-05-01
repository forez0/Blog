# blog/migrations/0005_post_author_alter_comment_author.py
"""Міграція: додає поле `author` до моделі Post та оновлює поле `author` у моделі Comment."""

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    """Додає поле `author` до Post і оновлює поле `author` у Comment (ForeignKey до User)."""

    dependencies = [
        ('blog', '0004_alter_comment_author'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='author',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='posts',
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name='comment',
            name='author',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='comments',
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]

