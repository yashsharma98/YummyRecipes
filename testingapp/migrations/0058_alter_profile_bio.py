# Generated by Django 4.0.4 on 2022-10-06 00:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testingapp', '0057_post_dislikes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='bio',
            field=models.TextField(default='Bio'),
        ),
    ]
