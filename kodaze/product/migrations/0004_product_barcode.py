# Generated by Django 4.0.7 on 2022-10-17 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_alter_product_company_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='barcode',
            field=models.PositiveIntegerField(blank=True, null=True, unique=True),
        ),
    ]
