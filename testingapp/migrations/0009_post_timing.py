# Generated by Django 4.0.4 on 2022-04-28 19:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testingapp', '0008_alter_post_image_alter_post_ingredients_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='timing',
            field=models.TextField(default=0),
        ),
    ]
