# Generated by Django 4.0.7 on 2022-12-25 18:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('holiday', '0013_alter_holidayoperation_holiday_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeedayoffoperation',
            name='day_off_date',
            field=models.CharField(max_length=800),
        ),
    ]
