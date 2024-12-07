# Generated by Django 5.0.6 on 2024-10-27 09:21

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('abonnement', '0001_initial'),
        ('client', '0001_initial'),
        ('creneau', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='abonnementclient',
            name='client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='abonnement_client', to='client.client'),
        ),
        migrations.AddField(
            model_name='abonnementclient',
            name='creneaux',
            field=models.ManyToManyField(blank=True, related_name='abonnements', to='creneau.creneau', verbose_name='créneau'),
        ),
        migrations.AddField(
            model_name='abonnementclient',
            name='type_abonnement',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='type_abonnement_client', to='abonnement.abonnement'),
        ),
        migrations.AddField(
            model_name='historicalabonnementclient',
            name='client',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='client.client'),
        ),
        migrations.AddField(
            model_name='historicalabonnementclient',
            name='history_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historicalabonnementclient',
            name='type_abonnement',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='abonnement.abonnement'),
        ),
    ]
