# Generated by Django 4.0.7 on 2022-09-22 13:48

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('task_manager', '0010_usertaskrequest_is_accept'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advertisement',
            name='created_date',
            field=models.DateField(blank=True, default=django.utils.timezone.now, null=True),
        ),
        migrations.AlterField(
            model_name='taskmanager',
            name='created_date',
            field=models.DateField(blank=True, default=django.utils.timezone.now, null=True),
        ),
        migrations.AlterField(
            model_name='taskmanager',
            name='end_date',
            field=models.DateField(),
        ),
    ]