# Generated by Django 3.2.9 on 2022-12-31 07:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contract', '0009_alter_contract_compensation_expense_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='installment',
            name='paid_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='installment',
            name='paid_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20),
        ),
    ]
