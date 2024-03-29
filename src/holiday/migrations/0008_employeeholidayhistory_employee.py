# Generated by Django 4.0.7 on 2022-12-01 15:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('holiday', '0007_rename_holiday_date_employeedayoffoperation_day_off_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='employeeholidayhistory',
            name='employee',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='holiday_histories', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
