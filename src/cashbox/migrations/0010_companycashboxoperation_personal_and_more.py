# Generated by Django 4.0.7 on 2022-11-20 18:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cashbox', '0009_cashflow_personal'),
    ]

    operations = [
        migrations.AddField(
            model_name='companycashboxoperation',
            name='personal',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='company_cashbox_operations_personals', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='holdingcashboxoperation',
            name='personal',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='holding_cashbox_operations_personals', to=settings.AUTH_USER_MODEL),
        ),
    ]
