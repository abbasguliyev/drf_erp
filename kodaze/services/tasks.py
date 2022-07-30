import datetime

from celery import shared_task
import pandas as pd
from contract.models import DemoSatis, Muqavile
from django.contrib.auth import get_user_model
from .models import Servis
from product.models import Mehsullar

User = get_user_model()

@shared_task(name='create_services_task')
def create_services_task(id):
    print(f"***************create_services_task task working******************")
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

    q = 0
    while(q<instance.mehsul_sayi):
        for i in range(1):
            servis_qiymeti = 0
            for j in kartric6ay:
                servis_qiymeti += float(j.qiymet)
            if(indi.day < 29):
                servis = Servis.objects.create(
                    muqavile=instance,
                    servis_tarix = f"{month6.year}-{month6.month}-{indi.day}",
                    servis_qiymeti=servis_qiymeti,
                    is_auto=True
                )
            elif(indi.day == 31 or indi.day == 30 or indi.day == 29):
                if(month6.day <= indi.day):
                    servis = Servis.objects.create(
                        muqavile=instance,
                        servis_tarix = f"{month6.year}-{month6.month}-{month6.day}",
                        servis_qiymeti=servis_qiymeti,
                        is_auto=True
                    )
                elif(month6.day > indi.day):
                    servis = Servis.objects.create(
                        muqavile=instance,
                        servis_tarix = f"{month6.year}-{month6.month}-{indi.day}",
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
                    servis_tarix = f"{month12.year}-{month12.month}-{indi.day}",
                    servis_qiymeti=servis_qiymeti,
                    is_auto=True
                )
            elif(indi.day == 31 or indi.day == 30 or indi.day == 29):
                if(month12.day <= indi.day):
                    servis = Servis.objects.create(
                        muqavile=instance,
                        servis_tarix = f"{month12.year}-{month12.month}-{month12.day}",
                        servis_qiymeti=servis_qiymeti,
                        is_auto=True
                    )
                elif(month12.day > indi.day):
                    servis = Servis.objects.create(
                        muqavile=instance,
                        servis_tarix = f"{month12.year}-{month12.month}-{indi.day}",
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
                    servis_tarix = f"{month18.year}-{month18.month}-{indi.day}",
                    servis_qiymeti=servis_qiymeti,
                    is_auto=True
                )
            elif(indi.day == 31 or indi.day == 30 or indi.day == 29):
                if(month18.day <= indi.day):
                    servis = Servis.objects.create(
                        muqavile=instance,
                        servis_tarix = f"{month18.year}-{month18.month}-{month18.day}",
                        servis_qiymeti=servis_qiymeti,
                        is_auto=True
                    )
                elif(month18.day > indi.day):
                    servis = Servis.objects.create(
                        muqavile=instance,
                        servis_tarix = f"{month18.year}-{month18.month}-{indi.day}",
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
                    servis_tarix = f"{month24.year}-{month24.month}-{indi.day}",
                    servis_qiymeti=servis_qiymeti,
                    is_auto=True
                )
            elif(indi.day == 31 or indi.day == 30 or indi.day == 29):
                if(month24.day <= indi.day):
                    servis = Servis.objects.create(
                        muqavile=instance,
                        servis_tarix = f"{month24.year}-{month24.month}-{month24.day}",
                        servis_qiymeti=servis_qiymeti,
                        is_auto=True
                    )
                elif(month24.day > indi.day):
                    servis = Servis.objects.create(
                        muqavile=instance,
                        servis_tarix = f"{month24.year}-{month24.month}-{indi.day}",
                        servis_qiymeti=servis_qiymeti,
                        is_auto=True
                    )
            servis.mehsullar.set(kartric24ay)
            servis.save()
        q+=1
