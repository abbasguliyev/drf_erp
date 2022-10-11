# Generated by Django 4.0.7 on 2022-10-11 08:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0003_office_unique name for your office constraint'),
        ('task_manager', '0003_remove_advertisement_position_advertisement_position'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advertisement',
            name='position',
            field=models.ManyToManyField(blank=True, related_name='advertisements', to='company.position'),
        ),
    ]
