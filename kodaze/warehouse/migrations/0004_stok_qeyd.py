# Generated by Django 3.2.12 on 2022-08-17 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('warehouse', '0003_stok_tarix'),
    ]

    operations = [
        migrations.AddField(
            model_name='stok',
            name='qeyd',
            field=models.TextField(blank=True, default='', null=True),
        ),
    ]
