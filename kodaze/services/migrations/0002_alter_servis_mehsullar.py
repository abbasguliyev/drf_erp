# Generated by Django 3.2.12 on 2022-08-04 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
        ('services', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='servis',
            name='mehsullar',
            field=models.ManyToManyField(related_name='servis_mehsul', to='product.Mehsullar'),
        ),
    ]