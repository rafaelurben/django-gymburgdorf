# Generated by Django 3.1.3 on 2020-11-29 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gymburgdorf', '0002_auto_20201129_1219'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='notenmanager',
            options={'verbose_name': 'Notenmanager', 'verbose_name_plural': 'Notenmanager'},
        ),
        migrations.AlterModelOptions(
            name='teilnote',
            options={'verbose_name': 'Teilnote', 'verbose_name_plural': 'Teilnoten'},
        ),
        migrations.AddField(
            model_name='note',
            name='beschreibung',
            field=models.CharField(default='', max_length=50, verbose_name='Beschreibung'),
        ),
    ]