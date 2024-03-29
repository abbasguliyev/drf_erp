# Generated by Django 4.0.7 on 2022-11-16 10:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transfer', '0003_remove_transferfromcompanytooffices_company_cashbox_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='companytransfer',
            old_name='previous_balance',
            new_name='recipient_subsequent_balance',
        ),
        migrations.RenameField(
            model_name='companytransfer',
            old_name='subsequent_balance',
            new_name='sender_subsequent_balance',
        ),
        migrations.RenameField(
            model_name='holdingtransfer',
            old_name='previous_balance',
            new_name='recipient_subsequent_balance',
        ),
        migrations.RenameField(
            model_name='holdingtransfer',
            old_name='subsequent_balance',
            new_name='sender_subsequent_balance',
        ),
        migrations.RenameField(
            model_name='officetransfer',
            old_name='previous_balance',
            new_name='recipient_subsequent_balance',
        ),
        migrations.RenameField(
            model_name='officetransfer',
            old_name='subsequent_balance',
            new_name='sender_subsequent_balance',
        ),
    ]
