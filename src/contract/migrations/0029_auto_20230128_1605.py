# Generated by Django 3.2.9 on 2023-01-28 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contract', '0028_alter_installment_note'),
    ]

    operations = [
        migrations.AddField(
            model_name='contract',
            name='contract_change_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='contract',
            name='contract_removed_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
