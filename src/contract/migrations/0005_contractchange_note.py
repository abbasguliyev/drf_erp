# Generated by Django 4.0.7 on 2022-10-14 20:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contract', '0004_alter_contract_initial_payment_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='contractchange',
            name='note',
            field=models.TextField(blank=True, null=True),
        ),
    ]
