# Generated by Django 3.2.9 on 2023-01-12 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contract', '0023_auto_20230112_1302'),
    ]

    operations = [
        migrations.AddField(
            model_name='contract',
            name='is_conditional_contract',
            field=models.BooleanField(default=False),
        ),
    ]
