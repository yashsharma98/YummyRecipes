# Generated by Django 4.0.4 on 2022-08-16 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testingapp', '0029_remove_post_udata'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='content',
            field=models.TextField(unique=True),
        ),
    ]