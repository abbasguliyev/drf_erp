# Generated by Django 3.2.12 on 2022-08-14 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_alter_bolge_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bolge',
            name='bolge_adi',
            field=models.CharField(max_length=300, unique=True),
        ),
    ]