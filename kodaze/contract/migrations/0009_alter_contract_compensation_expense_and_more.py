# Generated by Django 4.0.7 on 2022-12-05 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contract', '0008_alter_contract_initial_payment_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contract',
            name='compensation_expense',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20),
        ),
        migrations.AlterField(
            model_name='contract',
            name='compensation_income',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20),
        ),
        migrations.AlterField(
            model_name='contract',
            name='new_graphic_amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20),
        ),
        migrations.AlterField(
            model_name='contract',
            name='remaining_debt',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20),
        ),
        migrations.AlterField(
            model_name='contract',
            name='total_amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20),
        ),
        migrations.AlterField(
            model_name='installment',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20),
        ),
    ]
