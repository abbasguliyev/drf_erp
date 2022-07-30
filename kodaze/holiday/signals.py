from django.db.models.signals import post_save
from django.dispatch import receiver
import pandas as pd

import datetime
from company.models import Holding, Komanda, Ofis, Shirket, Shobe, Vezifeler
from .models import (
    HoldingGunler,
    KomandaGunler,
    OfisGunler,
    ShirketGunler,
    ShobeGunler,
    VezifeGunler
)

# Holding gunler ---------------------------------------------------
@receiver(post_save, sender=Holding)
def holding_gunler_create(sender, instance, created, **kwargs):
    """
    İş və tətil günlərini create edən task
    """
    if created:
        holding = instance
        indi = datetime.date.today()

        d = pd.to_datetime(f"{indi.year}-{indi.month}-{1}")

        next_m = d + pd.offsets.MonthBegin(1)

        days_in_this_month = pd.Period(f"{indi.year}-{indi.month}-{1}").days_in_month

        days_in_month = pd.Period(f"{next_m.year}-{next_m.month}-{1}").days_in_month

        holding_gunler = HoldingGunler.objects.filter(
            holding = holding,
            tarix__year = next_m.year,
            tarix__month = next_m.month
        )
        if len(holding_gunler) == 0:
            holding_gunler = HoldingGunler.objects.create(
                holding = holding,
                is_gunleri_count=days_in_month,
                tarix = f"{next_m.year}-{next_m.month}-{1}"
            )
            holding_gunler.save()
        
        holding_gunler = HoldingGunler.objects.filter(
            holding = holding,
            tarix__year = indi.year,
            tarix__month = indi.month
        )
        if len(holding_gunler) == 0:
            holding_gunler = HoldingGunler.objects.create(
                holding = holding,
                is_gunleri_count=days_in_this_month,
                tarix = f"{indi.year}-{indi.month}-{1}"
            )
            holding_gunler.save()

# Shirket gunler ---------------------------------------------------
@receiver(post_save, sender=Shirket)
def shirket_gunler_create(sender, instance, created, **kwargs):
    """
    İş və tətil günlərini create edən task
    """
    if created:
        shirket = instance
        indi = datetime.date.today()

        d = pd.to_datetime(f"{indi.year}-{indi.month}-{1}")

        next_m = d + pd.offsets.MonthBegin(1)

        days_in_this_month = pd.Period(f"{indi.year}-{indi.month}-{1}").days_in_month

        days_in_month = pd.Period(f"{next_m.year}-{next_m.month}-{1}").days_in_month

    
        shirket_gunler = ShirketGunler.objects.filter(
            shirket = shirket,
            tarix__year = next_m.year,
            tarix__month = next_m.month
        )
        if len(shirket_gunler) == 0:
            shirket_gunler = ShirketGunler.objects.create(
                shirket = shirket,
                is_gunleri_count=days_in_month,
                tarix = f"{next_m.year}-{next_m.month}-{1}"
            )
            shirket_gunler.save()
        
        shirket_gunler = ShirketGunler.objects.filter(
            shirket = shirket,
            tarix__year = indi.year,
            tarix__month = indi.month
        )
        if len(shirket_gunler) == 0:
            shirket_gunler = ShirketGunler.objects.create(
                shirket = shirket,
                is_gunleri_count=days_in_this_month,
                tarix = f"{indi.year}-{indi.month}-{1}"
            )
            shirket_gunler.save()

# Ofis gunler ---------------------------------------------------
@receiver(post_save, sender=Ofis)
def ofis_gunler_create(sender, instance, created, **kwargs):
    """
    İş və tətil günlərini create edən task
    """
    if created:
        ofis = instance
        indi = datetime.date.today()

        d = pd.to_datetime(f"{indi.year}-{indi.month}-{1}")

        next_m = d + pd.offsets.MonthBegin(1)

        days_in_this_month = pd.Period(f"{indi.year}-{indi.month}-{1}").days_in_month

        days_in_month = pd.Period(f"{next_m.year}-{next_m.month}-{1}").days_in_month

        ofis_gunler = OfisGunler.objects.filter(
            ofis = ofis,
            tarix__year = next_m.year,
            tarix__month = next_m.month
        )
        if len(ofis_gunler) == 0:
            ofis_gunler = OfisGunler.objects.create(
                ofis = ofis,
                is_gunleri_count=days_in_month,
                tarix = f"{next_m.year}-{next_m.month}-{1}"
            )
            ofis_gunler.save()

    
        ofis_gunler = OfisGunler.objects.filter(
            ofis = ofis,
            tarix__year = indi.year,
            tarix__month = indi.month
        )
        if len(ofis_gunler) == 0:
            ofis_gunler = OfisGunler.objects.create(
                ofis = ofis,
                is_gunleri_count=days_in_this_month,
                tarix = f"{indi.year}-{indi.month}-{1}"
            )
            ofis_gunler.save()

# Shobe gunler ---------------------------------------------------
@receiver(post_save, sender=Shobe)
def shobe_gunler_create(sender, instance, created, **kwargs):
    """
    İş və tətil günlərini create edən task
    """
    if created:
        shobe = instance
        indi = datetime.date.today()

        d = pd.to_datetime(f"{indi.year}-{indi.month}-{1}")

        next_m = d + pd.offsets.MonthBegin(1)

        days_in_this_month = pd.Period(f"{indi.year}-{indi.month}-{1}").days_in_month

        days_in_month = pd.Period(f"{next_m.year}-{next_m.month}-{1}").days_in_month

        shobe_gunler = ShobeGunler.objects.filter(
            shobe = shobe,
            tarix__year = next_m.year,
            tarix__month = next_m.month
        )
        if len(shobe_gunler) == 0:
            shobe_gunler = ShobeGunler.objects.create(
                shobe = shobe,
                is_gunleri_count=days_in_month,
                tarix = f"{next_m.year}-{next_m.month}-{1}"
            )
            shobe_gunler.save()
        shobe_gunler = ShobeGunler.objects.filter(
            shobe = shobe,
            tarix__year = indi.year,
            tarix__month = indi.month
        )
        if len(shobe_gunler) == 0:
            shobe_gunler = ShobeGunler.objects.create(
                shobe = shobe,
                is_gunleri_count=days_in_this_month,
                tarix = f"{indi.year}-{indi.month}-{1}"
            )
            shobe_gunler.save()

# Komanda gunler ---------------------------------------------------
@receiver(post_save, sender=Komanda)
def komanda_gunler_create(sender, instance, created, **kwargs):
    """
    İş və tətil günlərini create edən task
    """
    if created:
        komanda = instance
        indi = datetime.date.today()

        d = pd.to_datetime(f"{indi.year}-{indi.month}-{1}")

        next_m = d + pd.offsets.MonthBegin(1)

        days_in_this_month = pd.Period(f"{indi.year}-{indi.month}-{1}").days_in_month

        days_in_month = pd.Period(f"{next_m.year}-{next_m.month}-{1}").days_in_month

        komanda_gunler = KomandaGunler.objects.filter(
            komanda = komanda,
            tarix__year = next_m.year,
            tarix__month = next_m.month
        )
        if len(komanda_gunler) == 0:
            komanda_gunler = KomandaGunler.objects.create(
                komanda = komanda,
                is_gunleri_count=days_in_month,
                tarix = f"{next_m.year}-{next_m.month}-{1}"
            )
            komanda_gunler.save()
    
        komanda_gunler = KomandaGunler.objects.filter(
            komanda = komanda,
            tarix__year = indi.year,
            tarix__month = indi.month
        )
        if len(komanda_gunler) == 0:
            komanda_gunler = KomandaGunler.objects.create(
                komanda = komanda,
                is_gunleri_count=days_in_this_month,
                tarix = f"{indi.year}-{indi.month}-{1}"
            )
            komanda_gunler.save()

# Vezife gunler ---------------------------------------------------
@receiver(post_save, sender=Vezifeler)
def vezife_gunler_create(sender, instance, created, **kwargs):
    """
    İş və tətil günlərini create edən task
    """
    if created:
        vezife = instance
        indi = datetime.date.today()

        d = pd.to_datetime(f"{indi.year}-{indi.month}-{1}")

        next_m = d + pd.offsets.MonthBegin(1)

        days_in_this_month = pd.Period(f"{indi.year}-{indi.month}-{1}").days_in_month

        days_in_month = pd.Period(f"{next_m.year}-{next_m.month}-{1}").days_in_month


        vezife_gunler = VezifeGunler.objects.filter(
            vezife = vezife,
            tarix__year = next_m.year,
            tarix__month = next_m.month
        )
        if len(vezife_gunler) == 0:
            vezife_gunler = VezifeGunler.objects.create(
                vezife = vezife,
                is_gunleri_count=days_in_month,
                tarix = f"{next_m.year}-{next_m.month}-{1}"
            )
            vezife_gunler.save()
    
        vezife_gunler = VezifeGunler.objects.filter(
            vezife = vezife,
            tarix__year =  indi.year,
            tarix__month = indi.month
        )
        if len(vezife_gunler) == 0:
            vezife_gunler = VezifeGunler.objects.create(
                vezife = vezife,
                is_gunleri_count=days_in_this_month,
                tarix = f"{indi.year}-{indi.month}-{1}"
            )
            vezife_gunler.save()