# Generated by Django 3.2.9 on 2023-02-09 09:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backup_restore', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='backupandrestore',
            name='backup_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='backupandrestore',
            name='media_backup_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='backupandrestore',
            name='restore_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
