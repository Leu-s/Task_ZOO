# Generated by Django 3.2 on 2021-05-06 16:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_alter_aviary_free_area'),
    ]

    operations = [
        migrations.AddField(
            model_name='aviary',
            name='occupied_place',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='aviary',
            name='free_area',
            field=models.IntegerField(default=0),
        ),
    ]
