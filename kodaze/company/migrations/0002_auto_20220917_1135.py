# Generated by Django 3.2.12 on 2022-09-17 07:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ofis',
            name='ofis_adi',
            field=models.CharField(max_length=200),
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('departament_adi', models.CharField(max_length=200)),
                ('is_active', models.BooleanField(default=True)),
                ('shirket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='departaments', to='company.shirket')),
            ],
            options={
                'ordering': ('pk',),
                'permissions': (('view_ofis', 'Mövcud ofislərə baxa bilər'), ('add_ofis', 'Ofis əlavə edə bilər'), ('change_ofis', 'Ofis məlumatlarını yeniləyə bilər'), ('delete_ofis', 'Ofis silə bilər')),
                'default_permissions': [],
            },
        ),
    ]