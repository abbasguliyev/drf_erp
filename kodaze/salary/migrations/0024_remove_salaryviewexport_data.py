# Generated by Django 4.0.7 on 2022-11-16 10:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('salary', '0023_rename_file_name_salaryviewexport_file_data'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='salaryviewexport',
            name='data',
        ),
    ]
