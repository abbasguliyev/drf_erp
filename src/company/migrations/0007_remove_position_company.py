# Generated by Django 4.0.7 on 2022-10-18 12:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0006_remove_company_holding_remove_department_holding'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='position',
            name='company',
        ),
    ]
