# Generated by Django 3.2 on 2021-05-06 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_aviary_typeofanimals'),
    ]

    operations = [
        migrations.AddField(
            model_name='aviary',
            name='amount_animals',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='aviary',
            name='free_area',
            field=models.IntegerField(default=1, editable=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='aviary',
            name='required_area',
            field=models.FloatField(default=15),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Animal',
        ),
    ]
