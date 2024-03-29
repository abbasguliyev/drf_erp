# Generated by Django 4.0.7 on 2022-09-27 06:00

import core.image_validator
from django.conf import settings
import django.contrib.auth.validators
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('company', '__first__'),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fullname', models.CharField(max_length=200)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('profile_image', models.ImageField(blank=True, null=True, upload_to='media/%Y/%m/%d/', validators=[core.image_validator.file_size, django.core.validators.FileExtensionValidator(['png', 'jpeg', 'jpg'])])),
                ('photo_ID', models.ImageField(blank=True, null=True, upload_to='media/%Y/%m/%d/', validators=[core.image_validator.file_size, django.core.validators.FileExtensionValidator(['png', 'jpeg', 'jpg'])])),
                ('back_photo_of_ID', models.ImageField(blank=True, null=True, upload_to='media/%Y/%m/%d/', validators=[core.image_validator.file_size, django.core.validators.FileExtensionValidator(['png', 'jpeg', 'jpg'])])),
                ('phone_number_1', models.CharField(max_length=50)),
                ('phone_number_2', models.CharField(blank=True, max_length=50, null=True)),
                ('phone_number_3', models.CharField(blank=True, max_length=50, null=True)),
                ('phone_number_4', models.CharField(blank=True, max_length=50, null=True)),
                ('address', models.TextField(blank=True)),
                ('note', models.TextField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
            ],
            options={
                'ordering': ('pk',),
                'permissions': (('view_customer', 'Mövcud müştərilərə baxa bilər'), ('add_customer', 'Müştəri əlavə edə bilər'), ('change_customer', 'Müştəri məlumatlarını yeniləyə bilər'), ('delete_customer', 'Müştəri silə bilər')),
                'default_permissions': [],
            },
        ),
        migrations.CreateModel(
            name='EmployeeStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status_name', models.CharField(max_length=200)),
            ],
            options={
                'ordering': ('pk',),
                'permissions': (('view_employeestatus', 'Mövcud işçi statuslarına baxa bilər'), ('add_employeestatus', 'İşçi statusu əlavə edə bilər'), ('change_employeestatus', 'İşçi statusu məlumatlarını yeniləyə bilər'), ('delete_employeestatus', 'İşçi statusunu silə bilər')),
                'default_permissions': [],
            },
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('region_name', models.CharField(max_length=300, unique=True)),
            ],
            options={
                'ordering': ('pk',),
                'permissions': (('view_region', 'Mövcud bölgələrə baxa bilər'), ('add_region', 'Bölgə əlavə edə bilər'), ('change_region', 'Bölgə məlumatlarını yeniləyə bilər'), ('delete_region', 'Bölgə silə bilər')),
                'default_permissions': [],
            },
        ),
        migrations.CreateModel(
            name='CustomerNote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('note', models.TextField()),
                ('date', models.DateField(auto_now_add=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notes', to='account.customer')),
            ],
            options={
                'ordering': ('pk',),
                'permissions': (('view_customernote', 'Mövcud müştəri qeydlərinə baxa bilər'), ('add_customernote', 'Müştəri qeydi əlavə edə bilər'), ('change_customernote', 'Müştəri qeydinin məlumatlarını yeniləyə bilər'), ('delete_customernote', 'Müştəri qeydlərini silə bilər')),
                'default_permissions': [],
            },
        ),
        migrations.AddField(
            model_name='customer',
            name='region',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='account.region'),
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('fullname', models.CharField(max_length=200)),
                ('start_date_of_work', models.DateField(blank=True, default=django.utils.timezone.now, null=True)),
                ('dismissal_date', models.DateField(blank=True, null=True)),
                ('phone_number_1', models.CharField(max_length=200)),
                ('phone_number_2', models.CharField(blank=True, max_length=200, null=True)),
                ('photo_ID', models.ImageField(blank=True, null=True, upload_to='media/account/%Y/%m/%d/', validators=[core.image_validator.file_size, django.core.validators.FileExtensionValidator(['png', 'jpeg', 'jpg'])])),
                ('back_photo_of_ID', models.ImageField(blank=True, null=True, upload_to='media/account/%Y/%m/%d/', validators=[core.image_validator.file_size, django.core.validators.FileExtensionValidator(['png', 'jpeg', 'jpg'])])),
                ('driving_license_photo', models.ImageField(blank=True, null=True, upload_to='media/account/%Y/%m/%d/', validators=[core.image_validator.file_size, django.core.validators.FileExtensionValidator(['png', 'jpeg', 'jpg'])])),
                ('salary_style', models.CharField(choices=[('aylıq', 'aylıq'), ('günlük', 'günlük'), ('həftəlik', 'həftəlik'), ('fix', 'fix')], default='aylıq', max_length=50)),
                ('contract_type', models.CharField(blank=True, choices=[('xidməti müqavilə', 'xidməti müqavilə'), ('əmək müqaviləsi', 'əmək müqaviləsi')], default=None, max_length=50, null=True)),
                ('salary', models.FloatField(blank=True, default=0, null=True)),
                ('note', models.TextField(blank=True, null=True)),
                ('profile_image', models.ImageField(blank=True, null=True, upload_to='media/profile/%Y/%m/%d/', validators=[core.image_validator.file_size, django.core.validators.FileExtensionValidator(['png', 'jpeg', 'jpg'])])),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='employees', to='company.company')),
                ('department', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='employees', to='company.department')),
                ('employee_status', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='employees', to='account.employeestatus')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('office', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='employees', to='company.office')),
                ('position', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='employees', to='company.position')),
                ('section', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='employees', to='company.section')),
                ('supervisor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='employees', to=settings.AUTH_USER_MODEL)),
                ('tag', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='company.tag')),
                ('team', models.OneToOneField(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='employees', to='company.team')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'ordering': ('pk',),
                'permissions': (('view_user', 'Mövcud işçilərə baxa bilər'), ('add_user', 'İşçi əlavə edə bilər'), ('change_user', 'İşçi məlumatlarını yeniləyə bilər'), ('delete_user', 'İşçi silə bilər')),
                'default_permissions': [],
            },
        ),
    ]
