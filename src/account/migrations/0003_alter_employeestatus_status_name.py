# Generated by Django 4.0.7 on 2022-10-10 03:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_remove_user_tag_alter_user_back_photo_of_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeestatus',
            name='status_name',
            field=models.CharField(max_length=200, unique=True),
        ),
    ]
