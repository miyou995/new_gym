# Generated by Django 3.2.12 on 2022-09-21 19:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0010_auto_20220721_1412'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='is_on_salle',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='historicalclient',
            name='is_on_salle',
            field=models.BooleanField(default=True),
        ),
    ]
