# Generated by Django 3.2.5 on 2022-03-02 18:05

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('drf_app', '0005_auto_20220301_2041'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Creations',
            new_name='Box',
        ),
    ]
