# Generated by Django 3.2.9 on 2023-02-18 11:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0032_apppermission_update_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customgroup',
            name='group_type',
            field=models.CharField(blank=True, choices=[('İşçi', 'İşçi'), ('Tətil', 'Tətil'), ('İşçi icazə', 'İşçi icazə'), ('Komissiyalar', 'Komissiyalar'), ('Müqavilə', 'Müqavilə'), ('Müştəri', 'Müştəri'), ('Ə/H', 'Ə/H'), ('Avans', 'Avans'), ('Bonus', 'Bonus'), ('Cərimə', 'Cərimə'), ('Kəsinti', 'Kəsinti'), ('Balans', 'Balans'), ('Holding-şirkət', 'Holding-şirkət'), ('Şirkət-ofis', 'Şirkət-ofis'), ('Ofislərarası', 'Ofislərarası'), ('Ödəniş İzləmə', 'Ödəniş İzləmə'), ('Kassa Hərəkətləri', 'Kassa Hərəkətləri'), ('Holding əməliyyat', 'Holding əməliyyat'), ('Şirkət əməliyyat', 'Şirkət əməliyyat'), ('Xərc növləri', 'Xərc növləri'), ('Anbarlar', 'Anbarlar'), ('Məhsul', 'Məhsul'), ('Utilizasiya', 'Utilizasiya'), ('Holding Ofis Transfer', 'Holding Ofis Transfer'), ('Ofislər arası transfer', 'Ofislər arası transfer'), ('Ofis Holding Transfer', 'Ofis Holding Transfer'), ('Sorğu Göndər', 'Sorğu Göndər'), ('Ölçü Vahidi', 'Ölçü Vahidi'), ('Kateqoriyalar', 'Kateqoriyalar'), ('Tarixçə', 'Tarixçə'), ('Demo sayı', 'Demo sayı'), ('Satış sayı', 'Satış sayı'), ('Düşən satış sayı', 'Düşən satış sayı'), ('Düşmə faizi', 'Düşmə faizi'), ('Demo satış', 'Demo satış'), ('Demo iş günü', 'Demo iş günü'), ('Satış günü', 'Satış günü'), ('Tapşırıqlar', 'Tapşırıqlar'), ('Elanlar', 'Elanlar'), ('Servislər', 'Servislər'), ('Servis məhsullar', 'Servis məhsullar'), ('Holdinq parametrləri', 'Holdinq parametrləri')], max_length=255, null=True),
        ),
    ]
