# Generated by Django 4.1.5 on 2024-09-29 20:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('testingapp', '0081_remove_post_recipes_ranking_searchedrecipesranking'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='searchedrecipesranking',
            name='search_count',
        ),
    ]