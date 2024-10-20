# Generated by Django 3.1.6 on 2022-04-03 08:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('last_name', models.CharField(max_length=50, verbose_name='Nom')),
                ('first_name', models.CharField(max_length=50, verbose_name='Prénom')),
                ('civility', models.CharField(blank=True, choices=[('MLL', 'Mlle'), ('MME', 'Mme'), ('MR', 'Mr')], default='MME', max_length=3, null=True, verbose_name='Civilité')),
                ('adress', models.CharField(blank=True, max_length=200, null=True, verbose_name='Adresse')),
                ('picture', models.ImageField(blank=True, null=True, upload_to='photos')),
                ('phone', models.CharField(blank=True, max_length=22, null=True, verbose_name='Téléphone')),
                ('email', models.CharField(blank=True, max_length=50, null=True, verbose_name='E-mail')),
                ('nationality', models.CharField(blank=True, max_length=50, null=True, verbose_name='Nationalité')),
                ('birth_date', models.DateField(blank=True, max_length=50, null=True, verbose_name='Date de naissance')),
                ('blood', models.CharField(choices=[('A-', 'A-'), ('A+', 'A+'), ('B-', 'B-'), ('B+', 'B+'), ('O-', 'O-'), ('O+', 'O+'), ('AB-', 'AB-'), ('AB+', 'AB+')], max_length=3, verbose_name='Groupe sanguin')),
                ('date_added', models.DateField(auto_now_add=True)),
                ('profession', models.CharField(blank=True, max_length=50, null=True)),
                ('note', models.TextField(blank=True, null=True)),
                ('dette', models.DecimalField(blank=True, decimal_places=0, default=0, max_digits=10, null=True)),
                ('dette_assurance', models.DecimalField(blank=True, decimal_places=0, default=0, max_digits=10, null=True)),
                ('fin_assurance', models.DateField(blank=True, max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Coach',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_name', models.CharField(max_length=50, verbose_name='Nom')),
                ('first_name', models.CharField(max_length=50, verbose_name='Prénom')),
                ('civility', models.CharField(choices=[('MLL', 'Mlle'), ('MME', 'Mme'), ('MR', 'Mr')], default='MME', max_length=3, verbose_name='Civilité')),
                ('adress', models.CharField(blank=True, max_length=200, null=True, verbose_name='Adresse')),
                ('phone', models.CharField(blank=True, max_length=22, null=True, verbose_name='Téléphone')),
                ('email', models.CharField(blank=True, max_length=50, null=True, verbose_name='E-mail')),
                ('nationality', models.CharField(max_length=50, verbose_name='Nationalité')),
                ('birth_date', models.DateField(max_length=50, verbose_name='Date de naissance')),
                ('blood', models.CharField(choices=[('A-', 'A-'), ('A+', 'A+'), ('B-', 'B-'), ('B+', 'B+'), ('O-', 'O-'), ('O+', 'O+'), ('AB-', 'AB-'), ('AB+', 'AB+')], max_length=3, verbose_name='Groupe sanguin')),
                ('date_added', models.DateTimeField(auto_now_add=True, verbose_name="Date d'inscription")),
                ('state', models.CharField(choices=[('A', 'Active'), ('S', 'Suspendue'), ('N', 'Non active')], default='A', max_length=3, verbose_name='Etat')),
                ('note', models.TextField(blank=True, null=True)),
                ('salaire', models.DecimalField(blank=True, decimal_places=0, default=0, max_digits=10, null=True)),
                ('color', models.CharField(blank=True, default='#333333', max_length=50, null=True)),
                ('heures_done', models.IntegerField(blank=True, null=True)),
                ('pay_per_hour', models.IntegerField(blank=True, default=1, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Personnel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_name', models.CharField(max_length=50, verbose_name='Nom')),
                ('first_name', models.CharField(max_length=50, verbose_name='Prénom')),
                ('civility', models.CharField(choices=[('MLL', 'Mlle'), ('MME', 'Mme'), ('MR', 'Mr')], default='MME', max_length=3, verbose_name='Civilité')),
                ('adress', models.CharField(blank=True, max_length=200, null=True, verbose_name='Adresse')),
                ('phone', models.CharField(blank=True, max_length=22, null=True, verbose_name='Téléphone')),
                ('email', models.CharField(blank=True, max_length=50, null=True, verbose_name='E-mail')),
                ('nationality', models.CharField(max_length=50, verbose_name='Nationalité')),
                ('birth_date', models.DateField(max_length=50, verbose_name='Date de naissance')),
                ('blood', models.CharField(choices=[('A-', 'A-'), ('A+', 'A+'), ('B-', 'B-'), ('B+', 'B+'), ('O-', 'O-'), ('O+', 'O+'), ('AB-', 'AB-'), ('AB+', 'AB+')], max_length=3, verbose_name='Groupe sanguin')),
                ('date_added', models.DateTimeField(auto_now_add=True, verbose_name='Date de recrutement')),
                ('state', models.CharField(choices=[('A', 'Active'), ('S', 'Suspendue'), ('N', 'Non active')], default='A', max_length=3, verbose_name='Etat')),
                ('note', models.TextField(blank=True, null=True)),
                ('social_security', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='Maladie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('client', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='maladies', to='client.client')),
            ],
            options={
                'verbose_name': 'Maladie',
                'verbose_name_plural': 'Maladies',
            },
        ),
    ]
