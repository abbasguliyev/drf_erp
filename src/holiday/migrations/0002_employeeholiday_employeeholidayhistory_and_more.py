# Generated by Django 4.0.7 on 2022-11-26 15:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('company', '0008_remove_section_office'),
        ('holiday', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmployeeHoliday',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('holiday_date', models.DateField()),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='holidays', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='EmployeeHolidayHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateField(auto_now_add=True)),
                ('note', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='HolidayOperation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('holiday_date', models.CharField(max_length=350)),
                ('holding', models.BooleanField(default=False)),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='holiday_operations', to='company.company')),
                ('office', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='holiday_operations', to='company.office')),
                ('person_on_duty', models.ManyToManyField(related_name='person_on_duty', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='companyworkingday',
            name='company',
        ),
        migrations.RemoveField(
            model_name='employeearrivalanddeparturetimes',
            name='employee',
        ),
        migrations.RemoveField(
            model_name='holdingexceptionworker',
            name='exception_workers',
        ),
        migrations.RemoveField(
            model_name='holdingexceptionworker',
            name='working_day',
        ),
        migrations.RemoveField(
            model_name='holdingworkingday',
            name='holding',
        ),
        migrations.RemoveField(
            model_name='officeexceptionworker',
            name='exception_workers',
        ),
        migrations.RemoveField(
            model_name='officeexceptionworker',
            name='working_day',
        ),
        migrations.RemoveField(
            model_name='officeworkingday',
            name='office',
        ),
        migrations.RemoveField(
            model_name='positionexceptionworker',
            name='exception_workers',
        ),
        migrations.RemoveField(
            model_name='positionexceptionworker',
            name='working_day',
        ),
        migrations.RemoveField(
            model_name='positionworkingday',
            name='position',
        ),
        migrations.RemoveField(
            model_name='sectionexceptionworker',
            name='exception_workers',
        ),
        migrations.RemoveField(
            model_name='sectionexceptionworker',
            name='working_day',
        ),
        migrations.RemoveField(
            model_name='sectionworkingday',
            name='section',
        ),
        migrations.RemoveField(
            model_name='teamexceptionworker',
            name='exception_workers',
        ),
        migrations.RemoveField(
            model_name='teamexceptionworker',
            name='working_day',
        ),
        migrations.RemoveField(
            model_name='teamworkingday',
            name='team',
        ),
        migrations.AlterModelOptions(
            name='employeeworkingday',
            options={},
        ),
        migrations.RemoveField(
            model_name='employeeworkingday',
            name='date',
        ),
        migrations.RemoveField(
            model_name='employeeworkingday',
            name='holidays',
        ),
        migrations.RemoveField(
            model_name='employeeworkingday',
            name='is_paid',
        ),
        migrations.RemoveField(
            model_name='employeeworkingday',
            name='non_working_days_count',
        ),
        migrations.RemoveField(
            model_name='employeeworkingday',
            name='paid_leave_days',
        ),
        migrations.RemoveField(
            model_name='employeeworkingday',
            name='payment_amount',
        ),
        migrations.RemoveField(
            model_name='employeeworkingday',
            name='unpaid_leave_days',
        ),
        migrations.DeleteModel(
            name='CompanyExceptionWorker',
        ),
        migrations.DeleteModel(
            name='CompanyWorkingDay',
        ),
        migrations.DeleteModel(
            name='EmployeeArrivalAndDepartureTimes',
        ),
        migrations.DeleteModel(
            name='HoldingExceptionWorker',
        ),
        migrations.DeleteModel(
            name='HoldingWorkingDay',
        ),
        migrations.DeleteModel(
            name='OfficeExceptionWorker',
        ),
        migrations.DeleteModel(
            name='OfficeWorkingDay',
        ),
        migrations.DeleteModel(
            name='PositionExceptionWorker',
        ),
        migrations.DeleteModel(
            name='PositionWorkingDay',
        ),
        migrations.DeleteModel(
            name='SectionExceptionWorker',
        ),
        migrations.DeleteModel(
            name='SectionWorkingDay',
        ),
        migrations.DeleteModel(
            name='TeamExceptionWorker',
        ),
        migrations.DeleteModel(
            name='TeamWorkingDay',
        ),
        migrations.AddField(
            model_name='employeeholiday',
            name='history',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employee_holidays', to='holiday.employeeholidayhistory'),
        ),
    ]
