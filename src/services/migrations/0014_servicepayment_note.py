# Generated by Django 3.2.9 on 2023-01-20 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0013_alter_service_create_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='servicepayment',
            name='note',
            field=models.TextField(blank=True, default='', null=True),
        ),
    ]
