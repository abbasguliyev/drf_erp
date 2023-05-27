# Generated by Django 3.2.9 on 2023-02-16 07:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transfer', '0006_alter_companytransfer_recipient_subsequent_balance_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companytransfer',
            name='recipient_subsequent_balance',
            field=models.DecimalField(decimal_places=0, default=0, max_digits=20),
        ),
        migrations.AlterField(
            model_name='companytransfer',
            name='sender_subsequent_balance',
            field=models.DecimalField(decimal_places=0, default=0, max_digits=20),
        ),
        migrations.AlterField(
            model_name='companytransfer',
            name='transfer_amount',
            field=models.DecimalField(decimal_places=0, default=0, max_digits=20),
        ),
        migrations.AlterField(
            model_name='holdingtransfer',
            name='recipient_subsequent_balance',
            field=models.DecimalField(decimal_places=0, default=0, max_digits=20),
        ),
        migrations.AlterField(
            model_name='holdingtransfer',
            name='sender_subsequent_balance',
            field=models.DecimalField(decimal_places=0, default=0, max_digits=20),
        ),
        migrations.AlterField(
            model_name='holdingtransfer',
            name='transfer_amount',
            field=models.DecimalField(decimal_places=0, default=0, max_digits=20),
        ),
        migrations.AlterField(
            model_name='officetransfer',
            name='recipient_subsequent_balance',
            field=models.DecimalField(decimal_places=0, default=0, max_digits=20),
        ),
        migrations.AlterField(
            model_name='officetransfer',
            name='sender_subsequent_balance',
            field=models.DecimalField(decimal_places=0, default=0, max_digits=20),
        ),
        migrations.AlterField(
            model_name='officetransfer',
            name='transfer_amount',
            field=models.DecimalField(decimal_places=0, default=0, max_digits=20),
        ),
    ]