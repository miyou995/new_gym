# Generated by Django 3.2.12 on 2023-03-27 12:39

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('presence', '0003_historicalpresence_historicalpresencecoach'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalpresence',
            name='created',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, editable=False, verbose_name='Date de Création'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='historicalpresence',
            name='updated',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, editable=False, verbose_name='Date de dernière mise à jour'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='presence',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Date de Création'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='presence',
            name='updated',
            field=models.DateTimeField(auto_now=True, verbose_name='Date de dernière mise à jour'),
        ),
    ]
