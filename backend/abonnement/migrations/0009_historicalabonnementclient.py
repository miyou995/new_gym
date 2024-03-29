# Generated by Django 3.2.12 on 2022-05-04 13:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import simple_history.models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0009_historicalclient_historicalcoach_historicalpersonnel'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('abonnement', '0008_alter_abonnementclient_client'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalAbonnementClient',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('presence_quantity', models.IntegerField(blank=True, null=True)),
                ('reste', models.DecimalField(blank=True, decimal_places=0, max_digits=15, null=True, verbose_name='prix')),
                ('archiver', models.BooleanField(default=False)),
                ('created_date_time', models.DateTimeField(blank=True, editable=False)),
                ('updated_date_time', models.DateTimeField(blank=True, editable=False)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('client', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='client.client')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('type_abonnement', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='abonnement.abonnement')),
            ],
            options={
                'verbose_name': 'historical abonnement client',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]
