# Generated by Django 3.2.12 on 2022-04-11 21:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('creneau', '0004_auto_20220411_1357'),
    ]

    operations = [
        migrations.AlterField(
            model_name='creneau',
            name='day',
            field=models.CharField(choices=[('SA', 'Samedi'), ('DI', 'Dimanche'), ('LU', 'Lundi'), ('MA', 'Mardi'), ('ME', 'Mercredi'), ('JE', 'Jeudi'), ('VE', 'Vendredi')], default='DI', max_length=2, verbose_name='Jour'),
        ),
    ]
