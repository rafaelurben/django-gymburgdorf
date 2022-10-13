# Generated by Django 3.1.3 on 2020-12-12 16:50

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gymburgdorf', '0008_auto_20201211_1633'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fach',
            name='saved_value',
            field=models.FloatField(default=None, null=True, validators=[django.core.validators.MinValueValidator(1.0), django.core.validators.MaxValueValidator(6.0)], verbose_name='Notenwert'),
        ),
        migrations.AlterField(
            model_name='semester',
            name='saved_value',
            field=models.FloatField(default=None, null=True, validators=[django.core.validators.MinValueValidator(1.0), django.core.validators.MaxValueValidator(6.0)], verbose_name='Notenwert'),
        ),
    ]
