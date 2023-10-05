# Generated by Django 3.2.21 on 2023-10-05 08:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('warehouse', '0007_alter_warehouse_users'),
    ]

    operations = [
        migrations.AddField(
            model_name='mrsitem',
            name='loc',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='loc'),
        ),
        migrations.AlterField(
            model_name='mrsitem',
            name='condition',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='mrsitems', to='warehouse.condition', verbose_name='Condition'),
        ),
    ]