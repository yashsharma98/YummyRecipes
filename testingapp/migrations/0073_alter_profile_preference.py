# Generated by Django 4.1.5 on 2024-07-18 00:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testingapp', '0072_profile_preference'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='preference',
            field=models.CharField(blank=True, choices=[('Breakfast', 'Breakfast recipes'), ('lunch', 'Lunch recipes'), ('Snacks', 'Snacks recipes'), ('dinner', 'Dinner recipes'), ('veg', 'Veg recipes'), ('non_veg', 'Non-Veg recipes')], max_length=100, null=True),
        ),
    ]