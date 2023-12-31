# Generated by Django 3.2.21 on 2023-10-05 07:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20231005_0006'),
        ('warehouse', '0005_auto_20231005_0006'),
    ]

    operations = [
        migrations.CreateModel(
            name='Condition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='Condition')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='conditions', to='core.user', verbose_name='ثبت شده توسط')),
            ],
            options={
                'verbose_name': 'Condition',
                'verbose_name_plural': 'Conditions',
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='MaterialReceiptSheet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=200, verbose_name='MRS Number')),
                ('vendor', models.CharField(max_length=100, verbose_name='Vendor')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='mrs', to='core.user', verbose_name='ثبت شده توسط')),
                ('mr', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mrs', to='warehouse.materialrequisition', verbose_name='MR Number')),
                ('pl', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mrs', to='warehouse.packinglist', verbose_name='Packing List Number')),
                ('po', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mrs', to='warehouse.procurementorder', verbose_name='PO Number')),
                ('project', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='mrs', to='warehouse.project', verbose_name='Project')),
                ('warehouse', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mrs', to='warehouse.warehouse', verbose_name='Warehouse')),
            ],
            options={
                'verbose_name': 'Material Receipt Sheet',
                'verbose_name_plural': 'Material Receipt Sheets',
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='MRSItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.PositiveIntegerField(verbose_name='Mr Item No.')),
                ('quantity', models.DecimalField(decimal_places=3, max_digits=10, verbose_name='Quantity')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('condition', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mrsitems', to='warehouse.condition', verbose_name='Condition')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mrsitems', to='warehouse.item', verbose_name='Item Description')),
                ('mrs', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='warehouse.materialreceiptsheet')),
                ('unit', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='mrsitems', to='warehouse.unit', verbose_name='Unit')),
            ],
            options={
                'verbose_name': 'MRS Item',
                'verbose_name_plural': 'MRS Items',
            },
        ),
    ]
