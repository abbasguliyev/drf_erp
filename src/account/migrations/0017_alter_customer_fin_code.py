# Generated by Django 3.2.9 on 2023-01-03 09:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0016_auto_20230102_2121'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='fin_code',
            field=models.CharField(max_length=7, unique=True),
        ),
    ]
