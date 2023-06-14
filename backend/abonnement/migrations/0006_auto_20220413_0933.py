# Generated by Django 3.2.12 on 2022-04-13 08:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('abonnement', '0005_alter_abonnementclient_creneaux'),
    ]

    operations = [
        migrations.AlterField(
            model_name='abonnement',
            name='type_of',
            field=models.CharField(choices=[('VH', 'Volume Horaire'), ('AL', 'Accés Libre'), ('SF', 'Seances Fix'), ('SL', 'Seances Libre')], default='VH', max_length=2, verbose_name="type d'abonnement"),
        ),
        migrations.AlterField(
            model_name='abonnementclient',
            name='presence_quantity',
            field=models.DecimalField(blank=True, decimal_places='2', max_digits='8', null=True),
        ),
    ]
