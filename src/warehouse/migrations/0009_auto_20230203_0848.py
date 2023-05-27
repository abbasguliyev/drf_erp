# Generated by Django 3.2.9 on 2023-02-03 04:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('warehouse', '0008_rename_product_quantity_warehousehistory_quantity'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='holdingwarehouse',
            options={'default_permissions': [], 'ordering': ('-pk',), 'permissions': (('view_holdingwarehouse', 'Holding anbarına baxa bilər'),)},
        ),
        migrations.AlterModelOptions(
            name='stock',
            options={'default_permissions': [], 'ordering': ('-pk',), 'permissions': (('view_stock', 'Mövcud stoklara baxa bilər'), ('add_stock', 'Stock əlavə edə bilər'), ('change_stock', 'Stock məlumatlarını yeniləyə bilər'), ('delete_stock', 'Stock silə bilər'))},
        ),
        migrations.AlterModelOptions(
            name='warehouse',
            options={'default_permissions': [], 'ordering': ('-pk',), 'permissions': (('view_warehouse', 'Mövcud anbarlara baxa bilər'), ('add_warehouse', 'Anbar əlavə edə bilər'), ('change_warehouse', 'Anbar məlumatlarını yeniləyə bilər'), ('delete_warehouse', 'Anbar silə bilər'))},
        ),
    ]
