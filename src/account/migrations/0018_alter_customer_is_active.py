# Generated by Django 3.2.9 on 2023-01-03 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0017_alter_customer_fin_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
