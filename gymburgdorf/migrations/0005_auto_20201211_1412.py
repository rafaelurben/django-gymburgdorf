# Generated by Django 3.1.3 on 2020-12-11 13:12

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gymburgdorf', '0004_auto_20201129_1302'),
    ]

    operations = [
        migrations.AddField(
            model_name='fach',
            name='saved_value',
            field=models.FloatField(default=1.0, validators=[django.core.validators.MinValueValidator(1.0), django.core.validators.MaxValueValidator(6.0)], verbose_name='Notenwert'),
        ),
        migrations.AddField(
            model_name='note',
            name='saved_value',
            field=models.FloatField(default=1.0, validators=[django.core.validators.MinValueValidator(1.0), django.core.validators.MaxValueValidator(6.0)], verbose_name='Notenwert'),
        ),
        migrations.AddField(
            model_name='semester',
            name='saved_value',
            field=models.FloatField(default=1.0, validators=[django.core.validators.MinValueValidator(1.0), django.core.validators.MaxValueValidator(6.0)], verbose_name='Notenwert'),
        ),
        migrations.AlterField(
            model_name='semester',
            name='manager',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='semesters', to='gymburgdorf.notenmanager'),
        ),
    ]
