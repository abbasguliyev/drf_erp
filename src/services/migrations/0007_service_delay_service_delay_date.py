# Generated by Django 4.0.7 on 2022-12-21 07:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0006_alter_service_product_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='delay',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='service',
            name='delay_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
