# Generated by Django 3.2.21 on 2023-10-08 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('warehouse', '0012_auto_20231006_1955'),
    ]

    operations = [
        migrations.AddField(
            model_name='materialissuerequest',
            name='location',
            field=models.CharField(blank=True, max_length=100, verbose_name='Destination'),
        ),
    ]
