# Generated by Django 4.0.4 on 2022-05-04 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testingapp', '0016_alter_profile_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='gender',
            field=models.CharField(default='gender', max_length=20),
        ),
    ]
