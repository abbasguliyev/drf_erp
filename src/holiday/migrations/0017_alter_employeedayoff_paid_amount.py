# Generated by Django 3.2.9 on 2023-02-11 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('holiday', '0016_auto_20230203_0848'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeedayoff',
            name='paid_amount',
            field=models.DecimalField(decimal_places=0, default=0, max_digits=30),
        ),
    ]
