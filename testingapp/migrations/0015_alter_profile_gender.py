# Generated by Django 4.0.4 on 2022-05-04 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testingapp', '0014_post_cuisine_alter_post_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='gender',
            field=models.CharField(max_length=20),
        ),
    ]
