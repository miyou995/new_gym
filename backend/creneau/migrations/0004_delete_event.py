# Generated by Django 5.0.6 on 2024-10-24 12:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('creneau', '0003_alter_creneau_id_alter_event_id_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Event',
        ),
    ]
