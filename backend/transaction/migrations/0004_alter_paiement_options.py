# Generated by Django 5.0.6 on 2024-12-17 13:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0003_alter_paiement_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='paiement',
            options={'ordering': ['-last_modified']},
        ),
    ]
