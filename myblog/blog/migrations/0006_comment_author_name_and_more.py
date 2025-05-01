# blog/migrations/0006_comment_author_name_post_author_name_and_more.py

"""
This migration adds `author_name` fields to both the `Comment` and `Post` models
and updates the `author` field in both models to support nullable foreign keys
with a `SET_NULL` deletion rule.
"""

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    """
    This class defines the migration steps for adding `author_name` fields to the `Comment`
    and `Post` models and altering the `author` field in both models.
    """

    dependencies = [
        ('blog', '0005_post_author_alter_comment_author'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='author_name',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='post',
            name='author_name',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='comment',
            name='author',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='comments',
                to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AlterField(
            model_name='post',
            name='author',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='posts',
                to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
