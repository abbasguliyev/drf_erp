# Generated by Django 3.2.9 on 2023-01-11 20:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contract', '0021_alter_contract_initial_payment_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='contract',
            name='cancelled_contract',
            field=models.BooleanField(default=False),
        ),
    ]
