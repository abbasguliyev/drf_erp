# Generated by Django 3.2.9 on 2023-01-09 06:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contract', '0011_auto_20230102_2121'),
    ]

    operations = [
        migrations.AddField(
            model_name='contract',
            name='installment_start_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
