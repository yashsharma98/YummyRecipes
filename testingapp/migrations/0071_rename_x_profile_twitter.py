# Generated by Django 4.1.5 on 2024-07-17 14:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('testingapp', '0070_profile_x_profile_facebook_profile_instagram_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='X',
            new_name='twitter',
        ),
    ]
