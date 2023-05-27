# Generated by Django 3.2.9 on 2023-01-12 09:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0018_alter_customer_is_active'),
        ('contract', '0022_contract_cancelled_contract'),
    ]

    operations = [
        migrations.AddField(
            model_name='contract',
            name='address',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='contract',
            name='region',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='account.region'),
        ),
    ]
