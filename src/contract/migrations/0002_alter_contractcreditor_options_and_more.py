# Generated by Django 4.0.7 on 2022-10-12 15:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_alter_product_company_and_more'),
        ('contract', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contractcreditor',
            options={'default_permissions': [], 'ordering': ('-pk',), 'permissions': (('view_contractcreditor', 'Mövcud kreditorlara baxa bilər'), ('add_contractcreditor', 'Müqaviləyə kreditor əlavə edə bilər'), ('change_contractcreditor', 'Müqavilənin kreditor məlumatlarını yeniləyə bilər'), ('delete_contractcreditor', 'Müqavilənin kreditorunu silə bilər'))},
        ),
        migrations.AlterModelOptions(
            name='contractgift',
            options={'default_permissions': [], 'ordering': ('pk',), 'permissions': (('view_contractgift', 'Mövcud müqavilə hədiyyələrə baxa bilər'), ('add_contractgift', "Müqaviləy' hədiyyə əlavə edə bilər"), ('change_contractgift', 'Müqavilənin hədiyyə məlumatlarını yeniləyə bilər'), ('delete_contractgift', 'Müqavilənin hədiyyəsini silə bilər'))},
        ),
        migrations.RemoveField(
            model_name='contractgift',
            name='product',
        ),
        migrations.AddField(
            model_name='contractgift',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='gifts', to='product.product'),
        ),
    ]