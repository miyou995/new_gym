# Generated by Django 5.0.6 on 2024-12-16 15:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0002_alter_transaction_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='paiement',
            options={'ordering': ['-date_creation']},
        ),
    ]
