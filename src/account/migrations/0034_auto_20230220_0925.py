# Generated by Django 3.2.9 on 2023-02-20 05:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0009_auto_20230203_0848'),
        ('account', '0033_alter_customgroup_group_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customgroup',
            name='group_ptr',
        ),
        migrations.RemoveField(
            model_name='customgroup',
            name='menu_type',
        ),
        migrations.RemoveField(
            model_name='user',
            name='app_permission',
        ),
        migrations.DeleteModel(
            name='AppPermission',
        ),
        migrations.DeleteModel(
            name='CustomGroup',
        ),
        migrations.DeleteModel(
            name='MenuPermission',
        ),
    ]
