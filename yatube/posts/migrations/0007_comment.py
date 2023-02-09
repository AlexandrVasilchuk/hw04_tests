# Generated by Django 2.2.16 on 2023-02-08 12:49

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('posts', '0006_post_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                (
                    'id',
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'text',
                    models.TextField(
                        help_text='Оставьте свой комментарий',
                        verbose_name='комментарий',
                    ),
                ),
                (
                    'created',
                    models.DateTimeField(
                        auto_now_add=True, verbose_name='время комментария'
                    ),
                ),
                (
                    'author',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='comments',
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    'post',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='comments',
                        to='posts.Post',
                    ),
                ),
            ],
            options={
                'verbose_name': 'комментарий',
                'verbose_name_plural': 'комментарии',
                'ordering': ('-created',),
                'default_related_name': 'comments',
            },
        ),
    ]
