# Generated by Django 4.0.7 on 2022-09-27 06:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Update',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('update_name', models.CharField(max_length=150)),
                ('update_description', models.TextField()),
                ('update_version', models.CharField(max_length=100)),
            ],
            options={
                'ordering': ('-pk',),
            },
        ),
    ]
