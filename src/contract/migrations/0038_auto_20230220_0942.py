# Generated by Django 3.2.9 on 2023-02-20 05:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contract', '0037_auto_20230211_1632'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contract',
            name='new_graphic_amount',
        ),
        migrations.RemoveField(
            model_name='contract',
            name='new_graphic_status',
        ),
        migrations.RemoveField(
            model_name='installment',
            name='incomplete_month_substatus',
        ),
        migrations.RemoveField(
            model_name='installment',
            name='missed_month_substatus',
        ),
        migrations.AlterField(
            model_name='installment',
            name='payment_status',
            field=models.CharField(choices=[('ÖDƏNMƏYƏN', 'ÖDƏNMƏYƏN'), ('ÖDƏNƏN', 'ÖDƏNƏN')], default='ÖDƏNMƏYƏN', max_length=30),
        ),
    ]
