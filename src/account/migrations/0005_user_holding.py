# Generated by Django 4.0.7 on 2022-10-17 11:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0003_office_unique name for your office constraint'),
        ('account', '0004_alter_user_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='holding',
            field=models.ForeignKey(blank=True, help_text='Holdinq', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='employees', to='company.holding'),
        ),
    ]
