# Generated by Django 4.0.7 on 2022-12-05 12:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0014_alter_user_salary'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='salary',
            field=models.DecimalField(decimal_places=2, default=0, help_text='Ə/H', max_digits=10),
        ),
    ]
