# blog/migrations/0004_alter_comment_author.py
"""Оновлює поле `author` моделі Comment, встановлюючи зв'язок із моделлю User."""
# pylint: disable=duplicate-code

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    """Міграція для оновлення поля `author` у моделі Comment."""

    dependencies = [
        ('blog', '0003_comment'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
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
