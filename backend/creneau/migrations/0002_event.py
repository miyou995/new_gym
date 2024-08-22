# Generated by Django 5.0.6 on 2024-08-22 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('creneau', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
            ],
        ),
    ]
