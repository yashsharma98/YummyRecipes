# Generated by Django 4.0.4 on 2022-08-07 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testingapp', '0024_remove_profile_city_post_city'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='bio',
            field=models.TextField(default='Bio', max_length=200),
        ),
    ]