# Generated by Django 4.0.7 on 2022-12-01 05:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('salary', '0032_alter_salaryview_final_salary'),
    ]

    operations = [
        migrations.AlterField(
            model_name='salaryview',
            name='final_salary',
            field=models.FloatField(blank=True, default=0),
        ),
    ]