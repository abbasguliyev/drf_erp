# Generated by Django 3.2.9 on 2023-01-28 16:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0021_auto_20230128_1846'),
    ]

    operations = [
        migrations.CreateModel(
            name='AppPermission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('permission_name', models.CharField(max_length=255)),
                ('groups', models.ManyToManyField(related_name='permission_operations', to='account.CustomGroup')),
                ('menu', models.ManyToManyField(related_name='permission_operations', to='account.MenuPagination')),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='app_permission',
            field=models.ManyToManyField(related_name='employees', to='account.AppPermission'),
        ),
    ]
