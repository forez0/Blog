# blog/migrations/0002_post_image.py
"""Міграція для додавання поля image до моделі Post."""

from django.db import migrations, models


class Migration(migrations.Migration):
    """Додає поле image до моделі Post."""

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='image',
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to='posts/',
                verbose_name='Зображення'
            ),
        ),
    ]
