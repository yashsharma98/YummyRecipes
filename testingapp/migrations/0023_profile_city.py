# Generated by Django 4.0.4 on 2022-05-20 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testingapp', '0022_post_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='city',
            field=models.CharField(default='city', max_length=100),
        ),
    ]
