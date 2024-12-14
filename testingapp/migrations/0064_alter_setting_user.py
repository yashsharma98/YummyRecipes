# Generated by Django 4.0.4 on 2022-11-30 11:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('testingapp', '0063_setting_delete_choice'),
    ]

    operations = [
        migrations.AlterField(
            model_name='setting',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
