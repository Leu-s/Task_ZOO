# Generated by Django 3.2 on 2021-05-06 17:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_auto_20210506_1932'),
    ]

    operations = [
        migrations.AlterField(
            model_name='zoo',
            name='title',
            field=models.CharField(max_length=256, unique=True),
        ),
    ]
