# Generated by Django 4.0.4 on 2022-09-24 21:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('testingapp', '0049_like_created_like_updated_alter_post_likes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='like',
            name='created',
        ),
        migrations.RemoveField(
            model_name='like',
            name='updated',
        ),
    ]
