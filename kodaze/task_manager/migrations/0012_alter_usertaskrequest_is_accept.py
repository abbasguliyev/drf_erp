# Generated by Django 4.0.7 on 2022-09-22 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task_manager', '0011_alter_advertisement_created_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usertaskrequest',
            name='is_accept',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]