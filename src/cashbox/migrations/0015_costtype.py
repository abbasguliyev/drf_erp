# Generated by Django 3.2.9 on 2023-01-24 08:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cashbox', '0014_alter_cashflow_balance_alter_cashflow_quantity_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='CostType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'ordering': ('pk',),
                'permissions': (('view_costtype', 'Mövcud xərc növlərinə baxa bilər'), ('add_costtype', 'Xərc növü əlavə edə bilər'), ('change_costtype', 'Xərc növü məlumatlarını yeniləyə bilər'), ('delete_costtype', 'Xərc növü məlumatlarını silə bilər')),
                'default_permissions': [],
            },
        ),
    ]
