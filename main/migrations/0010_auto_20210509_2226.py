# Generated by Django 3.2 on 2021-05-09 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_auto_20210507_2234'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aviary',
            name='amount_animals',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='aviary',
            name='unit',
            field=models.CharField(choices=[('km2', 'Square kilometre'), ('m2', 'Square metre')], default='m2', max_length=20),
        ),
    ]
