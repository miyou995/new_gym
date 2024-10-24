# Generated by Django 3.2.12 on 2022-05-15 10:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('abonnement', '0009_historicalabonnementclient'),
        ('transaction', '0003_historicalassurancetransaction_historicalautre_historicalpaiement_historicalremuneration_historicalr'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paiement',
            name='abonnement_client',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='transactions', to='abonnement.abonnementclient'),
            preserve_default=False,
        ),
    ]
