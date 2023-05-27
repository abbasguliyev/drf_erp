# Generated by Django 4.0.7 on 2022-12-21 11:21

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('salary', '0026_alter_advancepayment_date_alter_bonus_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='advancepayment',
            name='salary_date',
            field=models.DateField(blank=True, default=django.utils.timezone.now, null=True),
        ),
        migrations.AddField(
            model_name='bonus',
            name='salary_date',
            field=models.DateField(blank=True, default=django.utils.timezone.now, null=True),
        ),
        migrations.AddField(
            model_name='salarydeduction',
            name='salary_date',
            field=models.DateField(blank=True, default=django.utils.timezone.now, null=True),
        ),
        migrations.AddField(
            model_name='salarypunishment',
            name='salary_date',
            field=models.DateField(blank=True, default=django.utils.timezone.now, null=True),
        ),
    ]
