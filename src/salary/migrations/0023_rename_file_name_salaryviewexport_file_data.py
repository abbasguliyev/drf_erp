# Generated by Django 4.0.7 on 2022-11-16 10:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('salary', '0022_rename_file_salaryviewexport_file_name_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='salaryviewexport',
            old_name='file_name',
            new_name='file_data',
        ),
    ]
