# Generated by Django 3.2.12 on 2022-09-17 06:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_auto_20220909_0635'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='maas_uslubu',
            field=models.CharField(choices=[('aylıq', 'aylıq'), ('günlük', 'günlük'), ('həftəlik', 'həftəlik'), ('fix', 'fix')], default='aylıq', max_length=50),
        ),
    ]