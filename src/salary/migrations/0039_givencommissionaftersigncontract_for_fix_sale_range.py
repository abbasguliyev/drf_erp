# Generated by Django 3.2.9 on 2023-02-08 08:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('salary', '0038_auto_20230208_1241'),
    ]

    operations = [
        migrations.AddField(
            model_name='givencommissionaftersigncontract',
            name='for_fix_sale_range',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20),
        ),
    ]