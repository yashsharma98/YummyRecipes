# Generated by Django 4.0.4 on 2022-08-21 04:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('testingapp', '0035_alter_post_author'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='FeedFile',
            new_name='photo',
        ),
    ]