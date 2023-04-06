# Generated by Django 3.2.12 on 2023-03-19 10:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('salle_activite', '0008_auto_20220724_1616'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='salle',
            name='door',
        ),
        migrations.AddField(
            model_name='door',
            name='door',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='doors', to='salle_activite.salle'),
        ),
    ]