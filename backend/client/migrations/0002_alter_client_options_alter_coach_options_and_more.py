# Generated by Django 5.0.6 on 2024-12-03 11:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='client',
            options={'ordering': ('-created',)},
        ),
        migrations.AlterModelOptions(
            name='coach',
            options={'ordering': ('-created',)},
        ),
        migrations.AlterModelOptions(
            name='personnel',
            options={'ordering': ('-created',)},
        ),
    ]
