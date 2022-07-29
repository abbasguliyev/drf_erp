from salary.models import MaasGoruntuleme
from account.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import datetime
import pandas as pd
from holiday.models import IsciGunler

@receiver(post_save, sender=User)
def create_isci_maas_goruntulenme(sender, instance, created, **kwargs):
    if created:
        user = instance
        indi = datetime.date.today()
        
        d = pd.to_datetime(f"{indi.year}-{indi.month}-{1}")
       
        next_m = d + pd.offsets.MonthBegin(1)
        
        isci_maas_bu_ay = MaasGoruntuleme.objects.filter(
            isci=user, 
            tarix__year = indi.year,
            tarix__month = indi.month
        )
        if len(isci_maas_bu_ay) == 0:
            if user.maas_uslubu == "FİX":
                MaasGoruntuleme.objects.create(isci=user, tarix=f"{indi.year}-{indi.month}-{1}", yekun_maas=user.maas).save()
            else:    
                MaasGoruntuleme.objects.create(isci=user, tarix=f"{indi.year}-{indi.month}-{1}").save()

        isci_maas_novbeti_ay = MaasGoruntuleme.objects.filter(
            isci=user, 
            tarix__year = next_m.year,
            tarix__month = next_m.month
        )
        if len(isci_maas_novbeti_ay) == 0:
            if user.maas_uslubu == "FİX":
                MaasGoruntuleme.objects.create(isci=user, tarix=f"{next_m.year}-{next_m.month}-{1}", yekun_maas=user.maas).save()
            else:    
                MaasGoruntuleme.objects.create(isci=user, tarix=f"{next_m.year}-{next_m.month}-{1}").save()

@receiver(post_save, sender=User)
def create_isci_gunler(sender, instance, created, **kwargs):
    if created:
        user = instance
        indi = datetime.date.today()

        d = pd.to_datetime(f"{indi.year}-{indi.month}-{1}")

        next_m = d + pd.offsets.MonthBegin(1)

        days_in_this_month = pd.Period(f"{indi.year}-{indi.month}-{1}").days_in_month

        days_in_mont = pd.Period(f"{next_m.year}-{next_m.month}-{1}").days_in_month
        
        isci_gunler_this_month = IsciGunler.objects.filter(
            isci = user,
            tarix__year = indi.year,
            tarix__month = indi.month
        )
        if len(isci_gunler_this_month) == 0:
            isci_gunler = IsciGunler.objects.create(
                isci = user,
                is_gunleri_count=days_in_this_month,
                tarix = f"{indi.year}-{indi.month}-{1}"
            )
            isci_gunler.save()

        isci_gunler = IsciGunler.objects.filter(
            isci = user,
            tarix__year = next_m.year,
            tarix__month = next_m.month
        )
        if len(isci_gunler) == 0:
            isci_gunler = IsciGunler.objects.create(
                isci = user,
                is_gunleri_count=days_in_mont,
                tarix = f"{next_m.year}-{next_m.month}-{1}"
            )
            isci_gunler.save()
