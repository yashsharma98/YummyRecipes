# Generated by Django 4.0.4 on 2022-08-22 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testingapp', '0040_remove_post_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='image',
            field=models.ManyToManyField(blank=True, null=True, to='testingapp.photo'),
        ),
    ]
