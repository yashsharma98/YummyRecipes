# Generated by Django 4.0.4 on 2022-05-08 07:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testingapp', '0019_alter_profile_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='gender',
            field=models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], max_length=20),
        ),
    ]