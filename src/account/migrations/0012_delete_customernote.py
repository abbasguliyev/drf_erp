# Generated by Django 4.0.7 on 2022-11-22 15:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0011_rename_contract_type_user_register_type'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CustomerNote',
        ),
    ]
