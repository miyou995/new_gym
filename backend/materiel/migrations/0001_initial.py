# Generated by Django 5.0.6 on 2024-10-27 09:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('salle_activite', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Materiel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='nom')),
                ('quantity', models.PositiveIntegerField()),
                ('note', models.CharField(blank=True, max_length=50, null=True, verbose_name='remarque')),
                ('inscription_date', models.DateField(auto_now_add=True, verbose_name="date d'ajout")),
                ('salle_activite', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='salle_activite.salle', verbose_name="salle d'activité")),
            ],
        ),
    ]
