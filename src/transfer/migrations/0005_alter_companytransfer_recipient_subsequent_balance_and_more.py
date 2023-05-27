# Generated by Django 4.0.7 on 2022-12-05 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transfer', '0004_rename_previous_balance_companytransfer_recipient_subsequent_balance_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companytransfer',
            name='recipient_subsequent_balance',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='companytransfer',
            name='sender_subsequent_balance',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='companytransfer',
            name='transfer_amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='holdingtransfer',
            name='recipient_subsequent_balance',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='holdingtransfer',
            name='sender_subsequent_balance',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='holdingtransfer',
            name='transfer_amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='officetransfer',
            name='recipient_subsequent_balance',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='officetransfer',
            name='sender_subsequent_balance',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='officetransfer',
            name='transfer_amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
