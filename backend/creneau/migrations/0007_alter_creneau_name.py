# Generated by Django 3.2.12 on 2022-04-11 21:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('creneau', '0006_creneau_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='creneau',
            name='name',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='nom du creneau'),
        ),
    ]
