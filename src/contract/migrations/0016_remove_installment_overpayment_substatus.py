# Generated by Django 3.2.9 on 2023-01-11 09:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contract', '0015_alter_installment_payment_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='installment',
            name='overpayment_substatus',
        ),
    ]
