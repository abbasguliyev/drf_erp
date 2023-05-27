# Generated by Django 4.0.7 on 2022-09-27 06:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('product', '0001_initial'),
        ('company', '0001_initial'),
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CreditorPrim',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prim_percent', models.PositiveBigIntegerField(blank=True, default=0)),
            ],
            options={
                'ordering': ('pk',),
                'permissions': (('view_creditorprim', 'Mövcud kreditor primlərə baxa bilər'), ('add_creditorprim', 'Kreditor prim əlavə edə bilər'), ('change_creditorprim', 'Kreditor prim məlumatlarını yeniləyə bilər'), ('delete_creditorprim', 'Kreditor prim silə bilər')),
                'default_permissions': [],
            },
        ),
        migrations.CreateModel(
            name='SalaryView',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField(blank=True, default=0)),
                ('note', models.TextField(blank=True, default='')),
                ('sale_quantity', models.PositiveBigIntegerField(blank=True, default=0)),
                ('sales_amount', models.FloatField(blank=True, default=0)),
                ('final_salary', models.FloatField(blank=True, default=0)),
                ('date', models.DateField(blank=True, null=True)),
                ('is_done', models.BooleanField(default=False)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employee_salary_views', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('pk',),
                'permissions': (('view_salaryview', 'Mövcud maaş cədvəllərinə baxa bilər'), ('add_salaryview', 'Maaş cədvəli əlavə edə bilər'), ('change_salaryview', 'Maaş cədvəlinin məlumatlarını yeniləyə bilər'), ('delete_salaryview', 'Maaş cədvəlini silə bilər')),
                'default_permissions': [],
            },
        ),
        migrations.CreateModel(
            name='SalaryDeduction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField(blank=True, default=0)),
                ('note', models.TextField(blank=True, default='')),
                ('date', models.DateField(blank=True, default=django.utils.timezone.now)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('pk',),
                'permissions': (('view_salarydeduction', 'Mövcud kəsintilərə baxa bilər'), ('add_salarydeduction', 'Kəsinti əlavə edə bilər'), ('change_salarydeduction', 'Kəsinti məlumatlarını yeniləyə bilər'), ('delete_salarydeduction', 'Kəsinti silə bilər')),
                'default_permissions': [],
            },
        ),
        migrations.CreateModel(
            name='PaySalary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField(blank=True, default=0)),
                ('note', models.TextField(blank=True, default='')),
                ('date', models.DateField(blank=True, default=django.utils.timezone.now)),
                ('installment', models.DateField(blank=True, default=django.utils.timezone.now, null=True)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('pk',),
                'permissions': (('view_paysalary', 'Mövcud maaş ödəmələrinə baxa bilər'), ('add_paysalary', 'Maaş ödəmə əlavə edə bilər'), ('change_paysalary', 'Maaş ödəmə məlumatlarını yeniləyə bilər'), ('delete_paysalary', 'Maaş ödəmə silə bilər')),
                'default_permissions': [],
            },
        ),
        migrations.CreateModel(
            name='OfficeLeaderPrim',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sales_amount', models.FloatField(blank=True, default=0, null=True)),
                ('prim_for_office', models.FloatField(blank=True, default=0)),
                ('fix_prim', models.FloatField(blank=True, default=0)),
                ('position', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='company.position')),
                ('prim_status', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='account.employeestatus')),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='product.product')),
            ],
            options={
                'ordering': ('pk',),
                'permissions': (('view_officeleaderprim', 'Mövcud ofis leader primlərə baxa bilər'), ('add_officeleaderprim', 'Ofis Leader prim əlavə edə bilər'), ('change_officeleaderprim', 'Ofis Leader prim məlumatlarını yeniləyə bilər'), ('delete_officeleaderprim', 'Ofis Leader prim silə bilər')),
                'default_permissions': [],
            },
        ),
        migrations.CreateModel(
            name='Manager2Prim',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sales_amount', models.FloatField(blank=True, default=0, null=True)),
                ('sale0', models.FloatField(blank=True, default=0)),
                ('sale1_8', models.FloatField(blank=True, default=0)),
                ('sale9_14', models.FloatField(blank=True, default=0)),
                ('sale15p', models.FloatField(blank=True, default=0)),
                ('sale20p', models.FloatField(blank=True, default=0)),
                ('prim_for_team', models.FloatField(blank=True, default=0)),
                ('prim_for_office', models.FloatField(blank=True, default=0)),
                ('fix_prim', models.FloatField(blank=True, default=0)),
                ('position', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='company.position')),
                ('prim_status', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='account.employeestatus')),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='product.product')),
            ],
            options={
                'ordering': ('pk',),
                'permissions': (('view_manager2prim', 'Mövcud manager2 primlərə baxa bilər'), ('add_manager2prim', 'Manager2 prim əlavə edə bilər'), ('change_manager2prim', 'Manager2 prim məlumatlarını yeniləyə bilər'), ('delete_manager2prim', 'Manager2 prim silə bilər')),
                'default_permissions': [],
            },
        ),
        migrations.CreateModel(
            name='Manager1PrimNew',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sales_amount', models.FloatField(blank=True, default=0, null=True)),
                ('cash', models.FloatField(blank=True, default=0)),
                ('installment_4_12', models.FloatField(blank=True, default=0)),
                ('installment_13_18', models.FloatField(blank=True, default=0)),
                ('installment_19_24', models.FloatField(blank=True, default=0)),
                ('position', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='company.position')),
                ('prim_status', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='account.employeestatus')),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='product.product')),
            ],
            options={
                'ordering': ('pk',),
                'permissions': (('view_manager1primnew', 'Mövcud manager1 primlərə baxa bilər'), ('add_manager1primnew', 'Manager1 prim əlavə edə bilər'), ('change_manager1primnew', 'Manager1 prim məlumatlarını yeniləyə bilər'), ('delete_manager1primnew', 'Manager1 prim silə bilər')),
                'default_permissions': [],
            },
        ),
        migrations.CreateModel(
            name='GroupLeaderPrimNew',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sales_amount', models.FloatField(blank=True, default=0, null=True)),
                ('cash', models.FloatField(blank=True, default=0)),
                ('installment_4_12', models.FloatField(blank=True, default=0)),
                ('installment_13_18', models.FloatField(blank=True, default=0)),
                ('installment_19_24', models.FloatField(blank=True, default=0)),
                ('position', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='company.position')),
                ('prim_status', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='account.employeestatus')),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='product.product')),
            ],
            options={
                'ordering': ('pk',),
                'permissions': (('view_groupleaderprimnew', 'Mövcud group leader primlərə baxa bilər'), ('add_groupleaderprimnew', 'GroupLeader prim əlavə edə bilər'), ('change_groupleaderprimnew', 'GroupLeader prim məlumatlarını yeniləyə bilər'), ('delete_groupleaderprimnew', 'GroupLeader prim silə bilər')),
                'default_permissions': [],
            },
        ),
        migrations.CreateModel(
            name='Bonus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField(blank=True, default=0)),
                ('note', models.TextField(blank=True, default='')),
                ('date', models.DateField(blank=True, default=django.utils.timezone.now)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('pk',),
                'permissions': (('view_bonus', 'Mövcud bonuslara baxa bilər'), ('add_bonus', 'Bonus əlavə edə bilər'), ('change_bonus', 'Bonus məlumatlarını yeniləyə bilər'), ('delete_bonus', 'Bonus silə bilər')),
                'default_permissions': [],
            },
        ),
        migrations.CreateModel(
            name='AdvancePayment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField(blank=True, default=0)),
                ('note', models.TextField(blank=True, default='')),
                ('date', models.DateField(blank=True, default=django.utils.timezone.now)),
                ('half_month_salary', models.PositiveBigIntegerField(blank=True, default=0)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('pk',),
                'permissions': (('view_advancepayment', 'Mövcud avanslara baxa bilər'), ('add_advancepayment', 'Avans əlavə edə bilər'), ('change_advancepayment', 'Avans məlumatlarını yeniləyə bilər'), ('delete_advancepayment', 'Avans silə bilər')),
                'default_permissions': [],
            },
        ),
    ]