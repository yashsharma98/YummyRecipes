# Generated by Django 4.0.4 on 2022-04-29 01:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('testingapp', '0011_post_types'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='types',
            new_name='type',
        ),
    ]
