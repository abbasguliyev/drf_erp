# Generated by Django 4.0.7 on 2022-11-16 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('salary', '0020_rename_is_done_advancepayment_is_paid_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='SalaryViewExport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='media/salary/%Y/%m/%d/')),
            ],
        ),
    ]
