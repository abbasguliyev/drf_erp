# Generated by Django 4.0.7 on 2022-10-24 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('salary', '0009_alter_commission_cash_alter_commission_for_office_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='monthrange',
            name='end_month',
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='salerange',
            name='end_count',
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
    ]