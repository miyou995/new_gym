# Generated by Django 5.0.6 on 2024-12-10 09:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('abonnement', '0002_abonnementclient_client_abonnementclient_creneaux_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='HistoricalAbonnementClient',
        ),
    ]
