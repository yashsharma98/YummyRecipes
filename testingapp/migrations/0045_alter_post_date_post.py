# Generated by Django 4.0.4 on 2022-09-11 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testingapp', '0044_alter_post_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='date_post',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]