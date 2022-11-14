# Generated by Django 4.0.7 on 2022-11-11 12:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('salary', '0018_alter_advancepayment_note_alter_bonus_note_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='advancepayment',
            name='is_done',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='bonus',
            name='is_done',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='paysalary',
            name='is_done',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='salarydeduction',
            name='is_done',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='salarypunishment',
            name='is_done',
            field=models.BooleanField(default=False),
        ),
    ]
