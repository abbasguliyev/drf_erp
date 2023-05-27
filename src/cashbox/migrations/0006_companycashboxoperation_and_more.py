# Generated by Django 4.0.7 on 2022-11-08 05:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0008_remove_section_office'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cashbox', '0005_remove_holdingcashboxoperation_previous_balance_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyCashboxOperation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField(default=0)),
                ('note', models.TextField(blank=True, null=True)),
                ('date', models.DateField(auto_now_add=True)),
                ('operation', models.CharField(choices=[('MƏDAXİL', 'MƏDAXİL'), ('MƏXARİC', 'MƏXARİC'), ('TRANSFER', 'TRANSFER')], default='MƏDAXİL', max_length=150)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='company_cashbox_operations', to='company.company')),
                ('executor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='company_cashbox_operations', to=settings.AUTH_USER_MODEL)),
                ('office', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='company_cashbox_operations', to='company.office')),
            ],
            options={
                'ordering': ('-pk',),
                'permissions': (('view_companycashboxoperation', 'Mövcud şirkət kassa əməliyyatlarına baxa bilər'), ('add_companycashboxoperation', 'Şirkət kassa əməliyyatı əlavə edə bilər'), ('change_companycashboxoperation', 'Şirkət kassa əməliyyatı məlumatlarını yeniləyə bilər'), ('delete_companycashboxoperation', 'Şirkət kassa əməliyyatı məlumatlarını silə bilər')),
                'default_permissions': [],
            },
        ),
        migrations.DeleteModel(
            name='OfficeCashboxOperation',
        ),
    ]
