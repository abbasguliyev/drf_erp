# Generated by Django 4.0.7 on 2022-09-27 06:00

import core.image_validator
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='AppLogo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('logo', models.ImageField(blank=True, null=True, upload_to='media/logo/%Y/%m/%d/', validators=[core.image_validator.file_size, django.core.validators.FileExtensionValidator(['png', 'jpeg', 'jpg'])])),
            ],
            options={
                'permissions': (('view_logo', 'Logoya baxa bilər'), ('add_logo', 'Logo əlavə edə bilər'), ('change_logo', 'Logonu yeniləyə bilər'), ('delete_logo', 'Logonu silə bilər')),
                'default_permissions': [],
            },
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(blank=True, default=True)),
                ('name', models.CharField(max_length=200, unique=True)),
            ],
            options={
                'ordering': ('pk',),
                'permissions': (('view_company', 'Mövcud şirkətlərə baxa bilər'), ('add_company', 'Şirkət əlavə edə bilər'), ('change_company', 'Şirkət məlumatlarını yeniləyə bilər'), ('delete_company', 'Şirkət silə bilər')),
                'default_permissions': [],
            },
        ),
        migrations.CreateModel(
            name='Holding',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(blank=True, default=True)),
                ('name', models.CharField(max_length=200, unique=True)),
            ],
            options={
                'ordering': ('pk',),
                'permissions': (('view_holding', 'Mövcud holdinqlərə baxa bilər'), ('add_holding', 'Holdinq əlavə edə bilər'), ('change_holding', 'Holdinq məlumatlarını yeniləyə bilər'), ('delete_holding', 'Holdinq silə bilər')),
                'default_permissions': [],
            },
        ),
        migrations.CreateModel(
            name='Office',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('is_active', models.BooleanField(blank=True, default=True)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='offices', to='company.company')),
            ],
            options={
                'ordering': ('pk',),
                'permissions': (('view_office', 'Mövcud ofislərə baxa bilər'), ('add_office', 'Ofis əlavə edə bilər'), ('change_office', 'Ofis məlumatlarını yeniləyə bilər'), ('delete_office', 'Ofis silə bilər')),
                'default_permissions': [],
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(blank=True, default=True)),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
            options={
                'ordering': ('pk',),
                'permissions': (('view_team', 'Mövcud komandalara baxa bilər'), ('add_team', 'Komanda əlavə edə bilər'), ('change_team', 'Komanda məlumatlarını yeniləyə bilər'), ('delete_team', 'Komanda silə bilər')),
                'default_permissions': [],
            },
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('is_active', models.BooleanField(blank=True, default=True)),
                ('office', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sections', to='company.office')),
            ],
            options={
                'ordering': ('pk',),
                'permissions': (('view_section', 'Mövcud şöbələrə baxa bilər'), ('add_section', 'Şöbə əlavə edə bilər'), ('change_section', 'Şöbə məlumatlarını yeniləyə bilər'), ('delete_section', 'Şöbə silə bilər')),
                'default_permissions': [],
            },
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('is_active', models.BooleanField(blank=True, default=True)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='positions', to='company.company')),
            ],
            options={
                'ordering': ('pk',),
                'permissions': (('view_position', 'Mövcud vəzifələrə baxa bilər'), ('add_position', 'Vəzifə əlavə edə bilər'), ('change_position', 'Vəzifə məlumatlarını yeniləyə bilər'), ('delete_position', 'Vəzifə silə bilər')),
                'default_permissions': [],
            },
        ),
        migrations.CreateModel(
            name='PermissionForPosition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('permission_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='permission_for_positions', to='auth.group')),
                ('position', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='permission_for_positions', to='company.position')),
            ],
            options={
                'ordering': ('pk',),
                'permissions': (('view_permissionforposition', 'Mövcud Vəzifə icazələrinə baxa bilər'), ('add_permissionforposition', 'Vəzifə icazə əlavə edə bilər'), ('change_permissionforposition', 'Vəzifə icazə məlumatlarını yeniləyə bilər'), ('delete_permissionforposition', 'Vəzifə icazə məlumatlarını silə bilər')),
                'default_permissions': [],
            },
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('is_active', models.BooleanField(blank=True, default=True)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='departments', to='company.company')),
            ],
            options={
                'ordering': ('pk',),
                'permissions': (('view_department', 'Mövcud departamentlərə baxa bilər'), ('add_department', 'Departament əlavə edə bilər'), ('change_department', 'Departament məlumatlarını yeniləyə bilər'), ('delete_department', 'Departament silə bilər')),
                'default_permissions': [],
            },
        ),
        migrations.AddField(
            model_name='company',
            name='holding',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='companies', to='company.holding'),
        ),
    ]
