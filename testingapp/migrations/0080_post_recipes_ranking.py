# Generated by Django 4.1.5 on 2024-09-29 19:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testingapp', '0079_alter_profile_preference_category_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='recipes_ranking',
            field=models.IntegerField(default=0),
        ),
    ]
