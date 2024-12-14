# Generated by Django 4.0.4 on 2022-09-22 20:06

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('testingapp', '0045_alter_post_date_post'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='likes',
            field=models.ManyToManyField(related_name='recipes', to=settings.AUTH_USER_MODEL),
        ),
    ]
