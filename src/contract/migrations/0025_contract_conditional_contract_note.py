# Generated by Django 3.2.9 on 2023-01-12 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contract', '0024_contract_is_conditional_contract'),
    ]

    operations = [
        migrations.AddField(
            model_name='contract',
            name='conditional_contract_note',
            field=models.TextField(blank=True, null=True),
        ),
    ]
