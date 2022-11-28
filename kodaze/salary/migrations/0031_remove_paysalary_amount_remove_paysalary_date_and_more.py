# Generated by Django 4.0.7 on 2022-11-28 11:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('salary', '0030_remove_paysalary_employee_paysalary_employee'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='paysalary',
            name='amount',
        ),
        migrations.RemoveField(
            model_name='paysalary',
            name='date',
        ),
        migrations.RemoveField(
            model_name='paysalary',
            name='employee',
        ),
        migrations.RemoveField(
            model_name='paysalary',
            name='is_paid',
        ),
        migrations.RemoveField(
            model_name='paysalary',
            name='note',
        ),
        migrations.RemoveField(
            model_name='paysalary',
            name='salary_date',
        ),
        migrations.AddField(
            model_name='paysalary',
            name='salary_view',
            field=models.ManyToManyField(to='salary.salaryview'),
        ),
    ]