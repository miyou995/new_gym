# Generated by Django 3.2.12 on 2022-04-10 08:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0002_auto_20220404_1532'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='maladie',
            name='client',
        ),
        migrations.AddField(
            model_name='client',
            name='maladies',
            field=models.ManyToManyField(to='client.Maladie'),
        ),
    ]
