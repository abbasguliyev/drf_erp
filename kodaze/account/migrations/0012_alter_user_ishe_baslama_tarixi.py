# Generated by Django 3.2.12 on 2022-08-19 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0011_alter_user_ishe_baslama_tarixi'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='ishe_baslama_tarixi',
            field=models.DateField(blank=True, null=True),
        ),
    ]
