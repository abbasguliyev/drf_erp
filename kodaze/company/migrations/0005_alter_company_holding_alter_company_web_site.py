# Generated by Django 4.0.7 on 2022-10-18 08:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0004_company_address_company_email_company_phone_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='holding',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='companies', to='company.holding'),
        ),
        migrations.AlterField(
            model_name='company',
            name='web_site',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
    ]