# Generated by Django 4.0.7 on 2022-11-28 11:09

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('salary', '0029_employeeactivityhistory_activity_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='paysalary',
            name='employee',
        ),
        migrations.AddField(
            model_name='paysalary',
            name='employee',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
