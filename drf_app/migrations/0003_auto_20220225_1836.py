# Generated by Django 3.2.5 on 2022-02-25 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drf_app', '0002_auto_20220224_1329'),
    ]

    operations = [
        migrations.AlterField(
            model_name='creations',
            name='area',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='creations',
            name='volume',
            field=models.IntegerField(),
        ),
    ]
