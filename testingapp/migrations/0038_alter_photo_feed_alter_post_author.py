# Generated by Django 4.0.4 on 2022-08-21 07:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('testingapp', '0037_alter_photo_feed_alter_post_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='feed',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='testingapp.post'),
        ),
        migrations.AlterField(
            model_name='post',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
