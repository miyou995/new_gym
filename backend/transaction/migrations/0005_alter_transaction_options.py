# Generated by Django 3.2.12 on 2022-09-19 14:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0004_alter_paiement_abonnement_client'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='transaction',
            options={'ordering': ['-last_modified'], 'permissions': [('can_view_history', 'Can View history')]},
        ),
    ]