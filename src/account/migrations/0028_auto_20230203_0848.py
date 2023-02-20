# Generated by Django 3.2.9 on 2023-02-03 04:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0027_user_fin_code'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customer',
            options={'default_permissions': [], 'ordering': ('-pk',), 'permissions': (('view_customer', 'Mövcud müştərilərə baxa bilər'), ('add_customer', 'Müştəri əlavə edə bilər'), ('change_customer', 'Müştəri məlumatlarını yeniləyə bilər'), ('delete_customer', 'Müştəri silə bilər'))},
        ),
        migrations.AlterModelOptions(
            name='employeeactivity',
            options={'default_permissions': [], 'ordering': ('-pk',), 'permissions': (('view_employeeactivity', 'Mövcud işçi müqavilə tarixçələrinə bilər'), ('add_employeeactivity', 'İşçi müqavilə tarixçəsi əlavə edə bilər'), ('change_employeeactivity', 'İşçi müqavilə tarixçəsi məlumatlarını yeniləyə bilər'), ('delete_employeeactivity', 'İşçi müqavilə tarixçəsi silə bilər'))},
        ),
        migrations.AlterModelOptions(
            name='user',
            options={'default_permissions': [], 'ordering': ('-pk',), 'permissions': (('view_user', 'Mövcud işçilərə baxa bilər'), ('add_user', 'İşçi əlavə edə bilər'), ('change_user', 'İşçi məlumatlarını yeniləyə bilər'), ('delete_user', 'İşçi silə bilər'))},
        ),
    ]
