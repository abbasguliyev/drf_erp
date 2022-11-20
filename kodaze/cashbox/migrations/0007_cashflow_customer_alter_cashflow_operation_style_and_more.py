# Generated by Django 4.0.7 on 2022-11-16 10:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_user_commission'),
        ('cashbox', '0006_companycashboxoperation_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='cashflow',
            name='customer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cash_flows', to='account.customer'),
        ),
        migrations.AlterField(
            model_name='cashflow',
            name='operation_style',
            field=models.CharField(blank=True, choices=[('MƏDAXİL', 'MƏDAXİL'), ('MƏXARİC', 'MƏXARİC')], default=None, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='companycashboxoperation',
            name='operation',
            field=models.CharField(choices=[('MƏDAXİL', 'MƏDAXİL'), ('MƏXARİC', 'MƏXARİC')], default='MƏDAXİL', max_length=150),
        ),
        migrations.AlterField(
            model_name='holdingcashboxoperation',
            name='operation',
            field=models.CharField(choices=[('MƏDAXİL', 'MƏDAXİL'), ('MƏXARİC', 'MƏXARİC')], default='MƏDAXİL', max_length=150),
        ),
    ]
