# Generated by Django 3.2.9 on 2023-01-11 08:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0009_alter_product_barcode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='barcode',
            field=models.PositiveBigIntegerField(blank=True, null=True),
        ),
    ]