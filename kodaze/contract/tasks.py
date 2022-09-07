import datetime

from celery import shared_task
import pandas as pd
from django.contrib.auth import get_user_model
from .models import DemoSatis, Muqavile, OdemeTarix
from services.models import Servis
from product.models import Mehsullar

User = get_user_model()

@shared_task(name='demo')
def demo_create_task():
    users = User.objects.all()

    indi = datetime.date.today()
    
    d = pd.to_datetime(f"{indi.year}-{indi.month}-{1}")

    next_m = d + pd.offsets.MonthBegin(1)


    for user in users:
        demos = DemoSatis.objects.filter(
            user = user,
            created_date__year = next_m.year,
            created_date__month = next_m.month
        )
        if len(demos) != 0:
            continue
        else:
            demo = DemoSatis.objects.create(user=user, count=0, created_date=f"{next_m.year}-{next_m.month}-{1}").save()
    
    for user in users:
        demos = DemoSatis.objects.filter(
            user = user,
            created_date__year = indi.year,
            created_date__month = indi.month
        )
        if len(demos) != 0:
            continue
        else:
            demo = DemoSatis.objects.create(user=user, count=0, created_date=f"{indi.year}-{indi.month}-{1}").save()

@shared_task(name='create_services_task')
def create_services_task(id):
    instance = Muqavile.objects.get(id=id)
    indi = instance.muqavile_tarixi

    d = pd.to_datetime(f"{indi.year}-{indi.month}-{indi.day}")
    month6 = pd.date_range(start=d, periods=2, freq='6M')[1]
    month12 = pd.date_range(start=d, periods=2, freq='12M')[1]
    month18 = pd.date_range(start=d, periods=2, freq='18M')[1]
    month24 = pd.date_range(start=d, periods=2, freq='24M')[1]
    
    kartric6ay = Mehsullar.objects.filter(kartric_novu="KARTRIC6AY", shirket=instance.shirket)
    kartric12ay = Mehsullar.objects.filter(kartric_novu="KARTRIC12AY", shirket=instance.shirket)
    kartric18ay = Mehsullar.objects.filter(kartric_novu="KARTRIC18AY", shirket=instance.shirket)
    kartric24ay = Mehsullar.objects.filter(kartric_novu="KARTRIC24AY", shirket=instance.shirket)

    date_format = '%d-%m-%Y'
    kartric6ay_date_lt_29 = datetime.datetime.strptime(f"{indi.day}-{month6.month}-{month6.year}", date_format)
    kartric6ay_date_eq_29_30_31 = datetime.datetime.strptime(f"{month6.day}-{month6.month}-{month6.year}", date_format)

    kartric12ay_date_lt_29 = datetime.datetime.strptime(f"{indi.day}-{month12.month}-{month12.year}", date_format)
    kartric12ay_date_eq_29_30_31 = datetime.datetime.strptime(f"{month12.day}-{month12.month}-{month12.year}", date_format)

    kartric18ay_date_lt_29 = datetime.datetime.strptime(f"{indi.day}-{month18.month}-{month18.year}", date_format)
    kartric18ay_date_eq_29_30_31 = datetime.datetime.strptime(f"{month18.day}-{month18.month}-{month18.year}", date_format)

    kartric24ay_date_lt_29 = datetime.datetime.strptime(f"{indi.day}-{month24.month}-{month24.year}", date_format)
    kartric24ay_date_eq_29_30_31 = datetime.datetime.strptime(f"{month24.day}-{month24.month}-{month24.year}", date_format)

    q = 0
    while(q<instance.mehsul_sayi):
        for i in range(1):
            servis_qiymeti = 0
            for j in kartric6ay:
                servis_qiymeti += float(j.qiymet)
            if(indi.day < 29):
                servis = Servis.objects.create(
                    muqavile=instance,
                    servis_tarix = kartric6ay_date_lt_29,
                    servis_qiymeti=servis_qiymeti,
                    is_auto=True
                )
            elif(indi.day == 31 or indi.day == 30 or indi.day == 29):
                if(month6.day <= indi.day):
                    servis = Servis.objects.create(
                        muqavile=instance,
                        servis_tarix = kartric6ay_date_eq_29_30_31,
                        servis_qiymeti=servis_qiymeti,
                        is_auto=True
                    )
                elif(month6.day > indi.day):
                    servis = Servis.objects.create(
                        muqavile=instance,
                        servis_tarix = kartric6ay_date_lt_29,
                        servis_qiymeti=servis_qiymeti,
                        is_auto=True
                    )
            servis.mehsullar.set(kartric6ay)
            servis.save()
        for i in range(1):
            servis_qiymeti = 0
            for j in kartric12ay:
                servis_qiymeti += float(j.qiymet)
            if(indi.day < 29):
                servis = Servis.objects.create(
                    muqavile=instance,
                    servis_tarix = kartric12ay_date_lt_29,
                    servis_qiymeti=servis_qiymeti,
                    is_auto=True
                )
            elif(indi.day == 31 or indi.day == 30 or indi.day == 29):
                if(month12.day <= indi.day):
                    servis = Servis.objects.create(
                        muqavile=instance,
                        servis_tarix = kartric12ay_date_eq_29_30_31,
                        servis_qiymeti=servis_qiymeti,
                        is_auto=True
                    )
                elif(month12.day > indi.day):
                    servis = Servis.objects.create(
                        muqavile=instance,
                        servis_tarix = kartric12ay_date_lt_29,
                        servis_qiymeti=servis_qiymeti,
                        is_auto=True
                    )
            servis.mehsullar.set(kartric12ay)
            servis.save()
        for i in range(1):
            servis_qiymeti = 0
            for j in kartric18ay:
                servis_qiymeti += float(j.qiymet)
            if(indi.day < 29):
                servis = Servis.objects.create(
                    muqavile=instance,
                    servis_tarix = kartric18ay_date_lt_29,
                    servis_qiymeti=servis_qiymeti,
                    is_auto=True
                )
            elif(indi.day == 31 or indi.day == 30 or indi.day == 29):
                if(month18.day <= indi.day):
                    servis = Servis.objects.create(
                        muqavile=instance,
                        servis_tarix = kartric18ay_date_eq_29_30_31,
                        servis_qiymeti=servis_qiymeti,
                        is_auto=True
                    )
                elif(month18.day > indi.day):
                    servis = Servis.objects.create(
                        muqavile=instance,
                        servis_tarix = kartric18ay_date_lt_29,
                        servis_qiymeti=servis_qiymeti,
                        is_auto=True
                    )
            servis.mehsullar.set(kartric18ay)
            servis.save()
        for i in range(1):
            servis_qiymeti = 0
            for j in kartric24ay:
                servis_qiymeti += float(j.qiymet)
            if(indi.day < 29):
                servis = Servis.objects.create(
                    muqavile=instance,
                    servis_tarix = kartric24ay_date_lt_29,
                    servis_qiymeti=servis_qiymeti,
                    is_auto=True
                )
            elif(indi.day == 31 or indi.day == 30 or indi.day == 29):
                if(month24.day <= indi.day):
                    servis = Servis.objects.create(
                        muqavile=instance,
                        servis_tarix = kartric24ay_date_eq_29_30_31,
                        servis_qiymeti=servis_qiymeti,
                        is_auto=True
                    )
                elif(month24.day > indi.day):
                    servis = Servis.objects.create(
                        muqavile=instance,
                        servis_tarix = kartric24ay_date_lt_29,
                        servis_qiymeti=servis_qiymeti,
                        is_auto=True
                    )
            servis.mehsullar.set(kartric24ay)
            servis.save()
        q+=1

@shared_task(name='create_odeme_tarix_task')
def create_odeme_tarix_task(id, created):
    instance = Muqavile.objects.get(id=id)
    kredit_muddeti = instance.kredit_muddeti
    mehsul_sayi = instance.mehsul_sayi
    
    def kredit_muddeti_func(kredit_muddeti, mehsul_sayi):
        kredit_muddeti_yeni = kredit_muddeti * mehsul_sayi
        return kredit_muddeti_yeni

    if(instance.odenis_uslubu == "KREDİT"):
        # indi = datetime.datetime.today().strftime('%d-%m-%Y')
        indi = instance.muqavile_tarixi
        inc_month = pd.date_range(indi, periods = kredit_muddeti+1, freq='M')
        ilkin_odenis = instance.ilkin_odenis
        ilkin_odenis_qaliq = instance.ilkin_odenis_qaliq

        if(ilkin_odenis is not None):
            ilkin_odenis = float(ilkin_odenis)
        
        if(ilkin_odenis_qaliq is not None):
            ilkin_odenis_qaliq = float(ilkin_odenis_qaliq)

        mehsulun_qiymeti = instance.muqavile_umumi_mebleg
        if(ilkin_odenis_qaliq == 0):
            ilkin_odenis_tam = ilkin_odenis
        elif(ilkin_odenis_qaliq != 0):
            ilkin_odenis_tam = ilkin_odenis + ilkin_odenis_qaliq
        aylara_gore_odenecek_umumi_mebleg = mehsulun_qiymeti - ilkin_odenis_tam
        
        if(kredit_muddeti > 0):
            aylara_gore_odenecek_mebleg = aylara_gore_odenecek_umumi_mebleg // kredit_muddeti

            qaliq = aylara_gore_odenecek_mebleg * (kredit_muddeti - 1)
            son_aya_odenecek_mebleg = aylara_gore_odenecek_umumi_mebleg - qaliq

            if created:
                i = 1
                while(i<=kredit_muddeti):
                    if(i == kredit_muddeti):
                        if(indi.day < 29):
                            OdemeTarix.objects.create(
                                ay_no = i,
                                muqavile = instance,
                                tarix = f"{inc_month[i].year}-{inc_month[i].month}-{indi.day}",
                                qiymet = son_aya_odenecek_mebleg,
                                sonuncu_ay = True
                            ).save()
                        elif(indi.day == 31 or indi.day == 30 or indi.day == 29):
                            if(inc_month[i].day <= indi.day):
                                OdemeTarix.objects.create(
                                    ay_no = i,
                                    muqavile = instance,
                                    tarix = f"{inc_month[i].year}-{inc_month[i].month}-{inc_month[i].day}",
                                    qiymet = son_aya_odenecek_mebleg,
                                    sonuncu_ay = True
                                ).save()
                            elif(inc_month[i].day > indi.day):
                                OdemeTarix.objects.create(
                                    ay_no = i,
                                    muqavile = instance,
                                    tarix = f"{inc_month[i].year}-{inc_month[i].month}-{indi.day}",
                                    qiymet = son_aya_odenecek_mebleg,
                                    sonuncu_ay = True
                                ).save()
                    else:
                        if(indi.day < 29):
                            OdemeTarix.objects.create(
                                ay_no = i,
                                muqavile = instance,
                                tarix = f"{inc_month[i].year}-{inc_month[i].month}-{indi.day}",
                                qiymet = aylara_gore_odenecek_mebleg
                            ).save()
                        elif(indi.day == 31 or indi.day == 30 or indi.day == 29):
                            if(inc_month[i].day <= indi.day):
                                OdemeTarix.objects.create(
                                    ay_no = i,
                                    muqavile = instance,
                                    tarix = f"{inc_month[i].year}-{inc_month[i].month}-{inc_month[i].day}",
                                    qiymet = aylara_gore_odenecek_mebleg
                                ).save()
                            if(inc_month[i].day > indi.day):
                                OdemeTarix.objects.create(
                                    ay_no = i,
                                    muqavile = instance,
                                    tarix = f"{inc_month[i].year}-{inc_month[i].month}-{indi.day}",
                                    qiymet = aylara_gore_odenecek_mebleg
                                ).save()
                    i+=1

@shared_task(name='demo_satis_sayi_task')
def demo_satis_sayi_task(id):
    instance = Muqavile.objects.get(id=id)
    menecer1 = instance.menecer1
    menecer2 = instance.menecer2
    muqavile_tarixi = instance.muqavile_tarixi
    mehsul_sayi = instance.mehsul_sayi
    sale_count = 0
    try:
        menecer1_demo = DemoSatis.objects.filter(user=menecer1, created_date=muqavile_tarixi)
        sale_count = sale_count + int(mehsul_sayi)
        menecer1_demo.sale_count = sale_count
        menecer1_demo.save()
    except:
        sale_count = 0
    try:
        menecer2_demo = DemoSatis.objects.filter(user=menecer2, created_date=muqavile_tarixi)
        sale_count = sale_count + int(mehsul_sayi)
        menecer2_demo.sale_count = sale_count
        menecer2_demo.save()
    except:
        sale_count = 0