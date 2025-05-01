# blog/migrations/0001_initial.py
"""Міграція для створення моделі Post."""

from django.db import migrations, models


class Migration(migrations.Migration):
    """Початкова міграція для створення моделі Post."""

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID'
                    )
                ),
                (
                    'title',
                    models.CharField(
                        max_length=200,
                        verbose_name='Заголовок',
                        blank=False
                    )
                ),
                (
                    'content',
                    models.TextField(
                        verbose_name='Вміст',
                        blank=False
                    )
                ),
                (
                    'created_at',
                    models.DateTimeField(
                        auto_now_add=True,
                        verbose_name='Дата створення'
                    )
                ),
                (
                    'updated_at',
                    models.DateTimeField(
                        auto_now=True,
                        verbose_name='Дата оновлення'
                    )
                ),
            ],
        ),
    ]
