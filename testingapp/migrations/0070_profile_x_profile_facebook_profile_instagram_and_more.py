# Generated by Django 4.1.5 on 2024-07-17 13:20

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testingapp', '0069_alter_post_content'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='X',
            field=models.URLField(blank=True, max_length=400, validators=[django.core.validators.URLValidator()]),
        ),
        migrations.AddField(
            model_name='profile',
            name='facebook',
            field=models.URLField(blank=True, max_length=400, validators=[django.core.validators.URLValidator()]),
        ),
        migrations.AddField(
            model_name='profile',
            name='instagram',
            field=models.URLField(blank=True, max_length=400, validators=[django.core.validators.URLValidator()]),
        ),
        migrations.AddField(
            model_name='profile',
            name='threads',
            field=models.URLField(blank=True, max_length=400, validators=[django.core.validators.URLValidator()]),
        ),
        migrations.AddField(
            model_name='profile',
            name='website',
            field=models.URLField(blank=True, max_length=400, validators=[django.core.validators.URLValidator()]),
        ),
        migrations.AddField(
            model_name='profile',
            name='youtube',
            field=models.URLField(blank=True, max_length=400, validators=[django.core.validators.URLValidator()]),
        ),
    ]