# Generated by Django 3.2.12 on 2022-05-04 13:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import simple_history.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('client', '0008_auto_20220418_0001'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalPersonnel',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('last_name', models.CharField(max_length=50, verbose_name='Nom')),
                ('first_name', models.CharField(max_length=50, verbose_name='Prénom')),
                ('civility', models.CharField(choices=[('MLL', 'Mlle'), ('MME', 'Mme'), ('MR', 'Mr')], default='MME', max_length=3, verbose_name='Civilité')),
                ('adress', models.CharField(blank=True, max_length=200, null=True, verbose_name='Adresse')),
                ('function', models.CharField(blank=True, max_length=200, null=True, verbose_name='Fonction')),
                ('phone', models.CharField(blank=True, max_length=22, null=True, verbose_name='Téléphone')),
                ('email', models.CharField(blank=True, max_length=50, null=True, verbose_name='E-mail')),
                ('nationality', models.CharField(max_length=50, verbose_name='Nationalité')),
                ('birth_date', models.DateField(max_length=50, verbose_name='Date de naissance')),
                ('blood', models.CharField(choices=[('A-', 'A-'), ('A+', 'A+'), ('B-', 'B-'), ('B+', 'B+'), ('O-', 'O-'), ('O+', 'O+'), ('AB-', 'AB-'), ('AB+', 'AB+')], max_length=3, verbose_name='Groupe sanguin')),
                ('date_added', models.DateTimeField(blank=True, editable=False, verbose_name='Date de recrutement')),
                ('created', models.DateTimeField(blank=True, editable=False, verbose_name='Date de Création')),
                ('updated', models.DateTimeField(blank=True, editable=False, verbose_name='Date de dernière mise à jour')),
                ('state', models.CharField(choices=[('A', 'Active'), ('S', 'Suspendue'), ('N', 'Non active')], default='A', max_length=3, verbose_name='Etat')),
                ('note', models.TextField(blank=True, null=True)),
                ('social_security', models.CharField(max_length=150)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical personnel',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalCoach',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('last_name', models.CharField(max_length=50, verbose_name='Nom')),
                ('first_name', models.CharField(max_length=50, verbose_name='Prénom')),
                ('civility', models.CharField(choices=[('MLL', 'Mlle'), ('MME', 'Mme'), ('MR', 'Mr')], default='MME', max_length=3, verbose_name='Civilité')),
                ('adress', models.CharField(blank=True, max_length=200, null=True, verbose_name='Adresse')),
                ('phone', models.CharField(blank=True, max_length=22, null=True, verbose_name='Téléphone')),
                ('email', models.CharField(blank=True, max_length=50, null=True, verbose_name='E-mail')),
                ('nationality', models.CharField(max_length=50, verbose_name='Nationalité')),
                ('birth_date', models.DateField(max_length=50, verbose_name='Date de naissance')),
                ('blood', models.CharField(choices=[('A-', 'A-'), ('A+', 'A+'), ('B-', 'B-'), ('B+', 'B+'), ('O-', 'O-'), ('O+', 'O+'), ('AB-', 'AB-'), ('AB+', 'AB+')], max_length=3, verbose_name='Groupe sanguin')),
                ('date_added', models.DateTimeField(blank=True, editable=False, verbose_name="Date d'inscription")),
                ('state', models.CharField(choices=[('A', 'Active'), ('S', 'Suspendue'), ('N', 'Non active')], default='A', max_length=3, verbose_name='Etat')),
                ('note', models.TextField(blank=True, null=True)),
                ('salaire', models.DecimalField(blank=True, decimal_places=0, default=0, max_digits=10, null=True)),
                ('color', models.CharField(blank=True, default='#333333', max_length=50, null=True)),
                ('heures_done', models.IntegerField(blank=True, null=True)),
                ('pay_per_hour', models.IntegerField(blank=True, default=1, null=True)),
                ('created', models.DateTimeField(blank=True, editable=False, verbose_name='Date de Création')),
                ('updated', models.DateTimeField(blank=True, editable=False, verbose_name='Date de dernière mise à jour')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical coach',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalClient',
            fields=[
                ('id', models.CharField(db_index=True, max_length=50)),
                ('carte', models.CharField(blank=True, db_index=True, max_length=100, null=True)),
                ('last_name', models.CharField(max_length=50, verbose_name='Nom')),
                ('first_name', models.CharField(max_length=50, verbose_name='Prénom')),
                ('civility', models.CharField(blank=True, choices=[('MLL', 'Mlle'), ('MME', 'Mme'), ('MR', 'Mr')], default='MME', max_length=3, null=True, verbose_name='Civilité')),
                ('adress', models.CharField(blank=True, max_length=200, null=True, verbose_name='Adresse')),
                ('picture', models.TextField(blank=True, max_length=100, null=True)),
                ('phone', models.CharField(blank=True, max_length=22, null=True, verbose_name='Téléphone')),
                ('email', models.CharField(blank=True, max_length=50, null=True, verbose_name='E-mail')),
                ('nationality', models.CharField(blank=True, max_length=50, null=True, verbose_name='Nationalité')),
                ('birth_date', models.DateField(blank=True, max_length=50, null=True, verbose_name='Date de naissance')),
                ('blood', models.CharField(choices=[('A-', 'A-'), ('A+', 'A+'), ('B-', 'B-'), ('B+', 'B+'), ('O-', 'O-'), ('O+', 'O+'), ('AB-', 'AB-'), ('AB+', 'AB+')], max_length=3, verbose_name='Groupe sanguin')),
                ('date_added', models.DateField(blank=True, editable=False)),
                ('created', models.DateTimeField(blank=True, editable=False, verbose_name='Date de Création')),
                ('profession', models.CharField(blank=True, max_length=50, null=True)),
                ('updated', models.DateTimeField(blank=True, editable=False, verbose_name='Date de dernière mise à jour')),
                ('note', models.TextField(blank=True, null=True)),
                ('dette', models.DecimalField(blank=True, decimal_places=0, default=0, max_digits=10, null=True)),
                ('dette_assurance', models.DecimalField(blank=True, decimal_places=0, default=0, max_digits=10, null=True)),
                ('fin_assurance', models.DateField(blank=True, max_length=50, null=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical client',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]
