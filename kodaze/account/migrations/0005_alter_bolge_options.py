# Generated by Django 3.2.12 on 2022-08-11 11:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_auto_20220811_1545'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bolge',
            options={'default_permissions': [], 'ordering': ('pk',), 'permissions': (('view_bolge', 'Mövcud bölgələrə baxa bilər'), ('add_bolge', 'Bölgə əlavə edə bilər'), ('change_bolge', 'Bölgə məlumatlarını yeniləyə bilər'), ('delete_bolge', 'Bölgə silə bilər'))},
        ),
    ]
