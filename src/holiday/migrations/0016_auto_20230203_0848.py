# Generated by Django 3.2.9 on 2023-02-03 04:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('holiday', '0015_alter_employeedayoff_paid_amount'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='employeedayoff',
            options={'default_permissions': [], 'ordering': ('-pk',), 'permissions': (('view_employeedayoff', 'Mövcud icazələrə baxa bilər'),)},
        ),
        migrations.AlterModelOptions(
            name='employeedayoffhistory',
            options={'default_permissions': [], 'ordering': ('-pk',), 'permissions': (('view_employeedayoffhistory', 'Mövcud icazə tarixçələrinə baxa bilər'), ('change_employeedayoffhistory', 'İcazə tarixçəsi məlumatlarını yeniləyə bilər'), ('delete_employeedayoffhistory', 'İcazə tarixçəsi silə bilər'))},
        ),
        migrations.AlterModelOptions(
            name='employeedayoffoperation',
            options={'default_permissions': [], 'ordering': ('-pk',), 'permissions': (('add_employeedayoffoperation', 'İcazə əlavə etmə əməliyyatı edə bilər'),)},
        ),
        migrations.AlterModelOptions(
            name='employeeholiday',
            options={'default_permissions': [], 'ordering': ('-pk',), 'permissions': (('view_employeeholiday', 'Mövcud tətillərə baxa bilər'),)},
        ),
        migrations.AlterModelOptions(
            name='employeeholidayhistory',
            options={'default_permissions': [], 'ordering': ('-pk',), 'permissions': (('view_employeeholidayhistory', 'Mövcud tətil tarixçələrinə baxa bilər'), ('change_employeeholidayhistory', 'Tətil tarixçəsi məlumatlarını yeniləyə bilər'), ('delete_employeeholidayhistory', 'Tətil tarixçəsi silə bilər'))},
        ),
        migrations.AlterModelOptions(
            name='employeeworkingday',
            options={'default_permissions': [], 'ordering': ('-pk',), 'permissions': (('view_employeeworkingday', 'İşçilərin iş qrafikinə baxa bilər'),)},
        ),
        migrations.AlterModelOptions(
            name='holidayoperation',
            options={'default_permissions': [], 'ordering': ('-pk',), 'permissions': (('add_holidayoperation', 'Tətil əlavə etmə əməliyyatı edə bilər'),)},
        ),
    ]
