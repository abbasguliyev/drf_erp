from celery import shared_task
import pandas as pd

import datetime
from account.models import User
from company.models import Holding, Komanda, Ofis, Shirket, Shobe, Vezifeler
from .models import (
    HoldingGunler,
    IsciGunler,
    KomandaGunler,
    OfisGunler,
    ShirketGunler,
    ShobeGunler,
    VezifeGunler
)

# Isci gunler ---------------------------------------------------
@shared_task(name='work_day_creater_task1')
def work_day_creater_task1():
    """
    İş və tətil günlərini create edən task
    """
    indi = datetime.date.today()

    d = pd.to_datetime(f"{indi.year}-{indi.month}-{1}")

    next_m = d + pd.offsets.MonthBegin(1)

    days_in_this_month = pd.Period(f"{indi.year}-{indi.month}-{1}").days_in_month

    days_in_month = pd.Period(f"{next_m.year}-{next_m.month}-{1}").days_in_month

    users = User.objects.all()

    for user in users:
        isci_gunler = IsciGunler.objects.filter(
            isci = user,
            tarix__year = next_m.year,
            tarix__month = next_m.month
        )
        if len(isci_gunler) != 0:
            continue
        else:
            isci_gunler = IsciGunler.objects.create(
                isci = user,
                is_gunleri_count=days_in_month,
                tarix = f"{next_m.year}-{next_m.month}-{1}"
            )
            isci_gunler.save()

    for user in users:
        isci_gunler = IsciGunler.objects.filter(
            isci = user,
            tarix__year = indi.year,
            tarix__month = indi.month
        )
        if len(isci_gunler) != 0:
            continue
        else:
            isci_gunler = IsciGunler.objects.create(
                isci = user,
                is_gunleri_count=days_in_this_month,
                tarix = f"{indi.year}-{indi.month}-{1}"
            )
            isci_gunler.save()


@shared_task(name='work_day_creater_task15')
def work_day_creater_task15():
    """
    İş və tətil günlərini create edən task
    """
    indi = datetime.date.today()

    d = pd.to_datetime(f"{indi.year}-{indi.month}-{1}")

    next_m = d + pd.offsets.MonthBegin(1)

    days_in_this_month = pd.Period(f"{indi.year}-{indi.month}-{1}").days_in_month

    days_in_month = pd.Period(f"{next_m.year}-{next_m.month}-{1}").days_in_month

    users = User.objects.all()

    for user in users:
        isci_gunler = IsciGunler.objects.filter(
            isci = user,
            tarix__year = next_m.year,
            tarix__month = next_m.month
        )
        if len(isci_gunler) != 0:
            continue
        else:
            isci_gunler = IsciGunler.objects.create(
                isci = user,
                is_gunleri_count=days_in_month,
                tarix = f"{next_m.year}-{next_m.month}-{1}"
            )
            isci_gunler.save()

    for user in users:
        isci_gunler = IsciGunler.objects.filter(
            isci = user,
            tarix__year = indi.year,
            tarix__month = indi.month
        )
        if len(isci_gunler) != 0:
            continue
        else:
            isci_gunler = IsciGunler.objects.create(
                isci = user,
                is_gunleri_count=days_in_this_month,
                tarix = f"{indi.year}-{indi.month}-{1}"
            )
            isci_gunler.save()

# Holding gunler ---------------------------------------------------
@shared_task(name='work_day_creater_holding_task1')
def work_day_creater_holding_task1():
    """
    İş və tətil günlərini create edən task
    """
    indi = datetime.date.today()

    d = pd.to_datetime(f"{indi.year}-{indi.month}-{1}")

    next_m = d + pd.offsets.MonthBegin(1)

    days_in_this_month = pd.Period(f"{indi.year}-{indi.month}-{1}").days_in_month

    days_in_month = pd.Period(f"{next_m.year}-{next_m.month}-{1}").days_in_month

    holdings = Holding.objects.all()

    for holding in holdings:
        holding_gunler = HoldingGunler.objects.filter(
            holding = holding,
            tarix__year = next_m.year,
            tarix__month = next_m.month
        )
        if len(holding_gunler) != 0:
            continue
        else:
            holding_gunler = HoldingGunler.objects.create(
                holding = holding,
                is_gunleri_count=days_in_month,
                tarix = f"{next_m.year}-{next_m.month}-{1}"
            )
            holding_gunler.save()
    
    for holding in holdings:
        holding_gunler = HoldingGunler.objects.filter(
            holding = holding,
            tarix__year = indi.year,
            tarix__month = indi.month
        )
        if len(holding_gunler) != 0:
            continue
        else:
            holding_gunler = HoldingGunler.objects.create(
                holding = holding,
                is_gunleri_count=days_in_this_month,
                tarix = f"{indi.year}-{indi.month}-{1}"
            )
            holding_gunler.save()

@shared_task(name='work_day_creater_holding_task15')
def work_day_creater_holding_task15():
    """
    İş və tətil günlərini create edən task
    """
    indi = datetime.date.today()

    d = pd.to_datetime(f"{indi.year}-{indi.month}-{1}")

    next_m = d + pd.offsets.MonthBegin(1)

    days_in_this_month = pd.Period(f"{indi.year}-{indi.month}-{1}").days_in_month

    days_in_month = pd.Period(f"{next_m.year}-{next_m.month}-{1}").days_in_month

    holdings = Holding.objects.all()

    for holding in holdings:
        holding_gunler = HoldingGunler.objects.filter(
            holding = holding,
            tarix__year = next_m.year,
            tarix__month = next_m.month
        )
        if len(holding_gunler) != 0:
            continue
        else:
            holding_gunler = HoldingGunler.objects.create(
                holding = holding,
                is_gunleri_count=days_in_month,
                tarix = f"{next_m.year}-{next_m.month}-{1}"
            )
            holding_gunler.save()
    for holding in holdings:
        holding_gunler = HoldingGunler.objects.filter(
            holding = holding,
            tarix__year = indi.year,
            tarix__month = indi.month
        )
        if len(holding_gunler) != 0:
            continue
        else:
            holding_gunler = HoldingGunler.objects.create(
                holding = holding,
                is_gunleri_count=days_in_this_month,
                tarix = f"{indi.year}-{indi.month}-{1}"
            )
            holding_gunler.save()

# Shirket gunler ---------------------------------------------------
@shared_task(name='work_day_creater_shirket_task1')
def work_day_creater_shirket_task1():
    """
    İş və tətil günlərini create edən task
    """
    indi = datetime.date.today()

    d = pd.to_datetime(f"{indi.year}-{indi.month}-{1}")

    next_m = d + pd.offsets.MonthBegin(1)

    days_in_this_month = pd.Period(f"{indi.year}-{indi.month}-{1}").days_in_month

    days_in_month = pd.Period(f"{next_m.year}-{next_m.month}-{1}").days_in_month

    shirketler = Shirket.objects.all()

    for shirket in shirketler:
        shirket_gunler = ShirketGunler.objects.filter(
            shirket = shirket,
            tarix__year = next_m.year,
            tarix__month = next_m.month
        )
        if len(shirket_gunler) != 0:
            continue
        else:
            shirket_gunler = ShirketGunler.objects.create(
                shirket = shirket,
                is_gunleri_count=days_in_month,
                tarix = f"{next_m.year}-{next_m.month}-{1}"
            )
            shirket_gunler.save()
    for shirket in shirketler:
        shirket_gunler = ShirketGunler.objects.filter(
            shirket = shirket,
            tarix__year = indi.year,
            tarix__month = indi.month
        )
        if len(shirket_gunler) != 0:
            continue
        else:
            shirket_gunler = ShirketGunler.objects.create(
                shirket = shirket,
                is_gunleri_count=days_in_this_month,
                tarix = f"{indi.year}-{indi.month}-{1}"
            )
            shirket_gunler.save()

@shared_task(name='work_day_creater_shirket_task15')
def work_day_creater_shirket_task15():
    """
    İş və tətil günlərini create edən task
    """
    indi = datetime.date.today()

    d = pd.to_datetime(f"{indi.year}-{indi.month}-{1}")

    next_m = d + pd.offsets.MonthBegin(1)

    days_in_this_month = pd.Period(f"{indi.year}-{indi.month}-{1}").days_in_month

    days_in_month = pd.Period(f"{next_m.year}-{next_m.month}-{1}").days_in_month

    shirketler = Shirket.objects.all()

    for shirket in shirketler:
        shirket_gunler = ShirketGunler.objects.filter(
            shirket = shirket,
            tarix__year = next_m.year,
            tarix__month = next_m.month
        )
        if len(shirket_gunler) != 0:
            continue
        else:
            shirket_gunler = ShirketGunler.objects.create(
                shirket = shirket,
                is_gunleri_count=days_in_month,
                tarix = f"{next_m.year}-{next_m.month}-{1}"
            )
            shirket_gunler.save()
    
    for shirket in shirketler:
        shirket_gunler = ShirketGunler.objects.filter(
            shirket = shirket,
            tarix__year = indi.year,
            tarix__month = indi.month
        )
        if len(shirket_gunler) != 0:
            continue
        else:
            shirket_gunler = ShirketGunler.objects.create(
                shirket = shirket,
                is_gunleri_count=days_in_this_month,
                tarix = f"{indi.year}-{indi.month}-{1}"
            )
            shirket_gunler.save()


# Ofis gunler ---------------------------------------------------
@shared_task(name='work_day_creater_ofis_task1')
def work_day_creater_ofis_task1():
    """
    İş və tətil günlərini create edən task
    """
    indi = datetime.date.today()

    d = pd.to_datetime(f"{indi.year}-{indi.month}-{1}")

    next_m = d + pd.offsets.MonthBegin(1)

    days_in_this_month = pd.Period(f"{indi.year}-{indi.month}-{1}").days_in_month

    days_in_month = pd.Period(f"{next_m.year}-{next_m.month}-{1}").days_in_month

    ofisler = Ofis.objects.all()

    for ofis in ofisler:
        ofis_gunler = OfisGunler.objects.filter(
            ofis = ofis,
            tarix__year = next_m.year,
            tarix__month = next_m.month
        )
        if len(ofis_gunler) != 0:
            continue
        else:
            ofis_gunler = OfisGunler.objects.create(
                ofis = ofis,
                is_gunleri_count=days_in_month,
                tarix = f"{next_m.year}-{next_m.month}-{1}"
            )
            ofis_gunler.save()

    for ofis in ofisler:
        ofis_gunler = OfisGunler.objects.filter(
            ofis = ofis,
            tarix__year = indi.year,
            tarix__month = indi.month
        )
        if len(ofis_gunler) != 0:
            continue
        else:
            ofis_gunler = OfisGunler.objects.create(
                ofis = ofis,
                is_gunleri_count=days_in_this_month,
                tarix = f"{indi.year}-{indi.month}-{1}"
            )
            ofis_gunler.save()

@shared_task(name='work_day_creater_ofis_task15')
def work_day_creater_ofis_task15():
    """
    İş və tətil günlərini create edən task
    """
    indi = datetime.date.today()

    d = pd.to_datetime(f"{indi.year}-{indi.month}-{1}")

    next_m = d + pd.offsets.MonthBegin(1)

    days_in_this_month = pd.Period(f"{indi.year}-{indi.month}-{1}").days_in_month

    days_in_month = pd.Period(f"{next_m.year}-{next_m.month}-{1}").days_in_month

    ofisler = Ofis.objects.all()

    for ofis in ofisler:
        ofis_gunler = OfisGunler.objects.filter(
            ofis = ofis,
            tarix__year = next_m.year,
            tarix__month = next_m.month
        )
        if len(ofis_gunler) != 0:
            continue
        else:
            ofis_gunler = OfisGunler.objects.create(
                ofis = ofis,
                is_gunleri_count=days_in_month,
                tarix = f"{next_m.year}-{next_m.month}-{1}"
            )
            ofis_gunler.save()
    for ofis in ofisler:
        ofis_gunler = OfisGunler.objects.filter(
            ofis = ofis,
            tarix__year = indi.year,
            tarix__month = indi.month
        )
        if len(ofis_gunler) != 0:
            continue
        else:
            ofis_gunler = OfisGunler.objects.create(
                ofis = ofis,
                is_gunleri_count=days_in_this_month,
                tarix = f"{indi.year}-{indi.month}-{1}"
            )
            ofis_gunler.save()

# Shobe gunler ---------------------------------------------------
@shared_task(name='work_day_creater_shobe_task1')
def work_day_creater_shobe_task1():
    """
    İş və tətil günlərini create edən task
    """
    indi = datetime.date.today()

    d = pd.to_datetime(f"{indi.year}-{indi.month}-{1}")

    next_m = d + pd.offsets.MonthBegin(1)

    days_in_this_month = pd.Period(f"{indi.year}-{indi.month}-{1}").days_in_month

    days_in_month = pd.Period(f"{next_m.year}-{next_m.month}-{1}").days_in_month

    shobeler = Shobe.objects.all()

    for shobe in shobeler:
        shobe_gunler = ShobeGunler.objects.filter(
            shobe = shobe,
            tarix__year = next_m.year,
            tarix__month = next_m.month
        )
        if len(shobe_gunler) != 0:
            continue
        else:
            shobe_gunler = ShobeGunler.objects.create(
                shobe = shobe,
                is_gunleri_count=days_in_month,
                tarix = f"{next_m.year}-{next_m.month}-{1}"
            )
            shobe_gunler.save()
    for shobe in shobeler:
        shobe_gunler = ShobeGunler.objects.filter(
            shobe = shobe,
            tarix__year = indi.year,
            tarix__month = indi.month
        )
        if len(shobe_gunler) != 0:
            continue
        else:
            shobe_gunler = ShobeGunler.objects.create(
                shobe = shobe,
                is_gunleri_count=days_in_this_month,
                tarix = f"{indi.year}-{indi.month}-{1}"
            )
            shobe_gunler.save()

@shared_task(name='work_day_creater_shobe_task15')
def work_day_creater_shobe_task15():
    """
    İş və tətil günlərini create edən task
    """
    indi = datetime.date.today()

    d = pd.to_datetime(f"{indi.year}-{indi.month}-{1}")

    next_m = d + pd.offsets.MonthBegin(1)

    days_in_this_month = pd.Period(f"{indi.year}-{indi.month}-{1}").days_in_month

    days_in_month = pd.Period(f"{next_m.year}-{next_m.month}-{1}").days_in_month

    shobeler = Shobe.objects.all()

    for shobe in shobeler:
        shobe_gunler = ShobeGunler.objects.filter(
            shobe = shobe,
            tarix__year = next_m.year,
            tarix__month = next_m.month
        )
        if len(shobe_gunler) != 0:
            continue
        else:
            shobe_gunler = ShobeGunler.objects.create(
                shobe = shobe,
                is_gunleri_count=days_in_month,
                tarix = f"{next_m.year}-{next_m.month}-{1}"
            )
            shobe_gunler.save()
    
    for shobe in shobeler:
        shobe_gunler = ShobeGunler.objects.filter(
            shobe = shobe,
            tarix__year = indi.year,
            tarix__month = indi.month
        )
        if len(shobe_gunler) != 0:
            continue
        else:
            shobe_gunler = ShobeGunler.objects.create(
                shobe = shobe,
                is_gunleri_count=days_in_this_month,
                tarix = f"{indi.year}-{indi.month}-{1}"
            )
            shobe_gunler.save()


# Komanda gunler ---------------------------------------------------
@shared_task(name='work_day_creater_komanda_task1')
def work_day_creater_komanda_task1():
    """
    İş və tətil günlərini create edən task
    """
    indi = datetime.date.today()

    d = pd.to_datetime(f"{indi.year}-{indi.month}-{1}")

    next_m = d + pd.offsets.MonthBegin(1)

    days_in_this_month = pd.Period(f"{indi.year}-{indi.month}-{1}").days_in_month

    days_in_month = pd.Period(f"{next_m.year}-{next_m.month}-{1}").days_in_month

    komandalar = Komanda.objects.all()

    vezife = Vezifeler.objects.all()

    for komanda in komandalar:
        komanda_gunler = KomandaGunler.objects.filter(
            komanda = komanda,
            tarix__year = next_m.year,
            tarix__month = next_m.month
        )
        if len(komanda_gunler) != 0:
            continue
        else:
            komanda_gunler = KomandaGunler.objects.create(
                komanda = komanda,
                is_gunleri_count=days_in_month,
                tarix = f"{next_m.year}-{next_m.month}-{1}"
            )
            komanda_gunler.save()
    
    for komanda in komandalar:
        komanda_gunler = KomandaGunler.objects.filter(
            komanda = komanda,
            tarix__year = indi.year,
            tarix__month = indi.month
        )
        if len(komanda_gunler) != 0:
            continue
        else:
            komanda_gunler = KomandaGunler.objects.create(
                komanda = komanda,
                is_gunleri_count=days_in_this_month,
                tarix = f"{indi.year}-{indi.month}-{1}"
            )
            komanda_gunler.save()

@shared_task(name='work_day_creater_komanda_task15')
def work_day_creater_komanda_task15():
    """
    İş və tətil günlərini create edən task
    """
    indi = datetime.date.today()

    d = pd.to_datetime(f"{indi.year}-{indi.month}-{1}")

    next_m = d + pd.offsets.MonthBegin(1)

    days_in_this_month = pd.Period(f"{indi.year}-{indi.month}-{1}").days_in_month

    days_in_month = pd.Period(f"{next_m.year}-{next_m.month}-{1}").days_in_month

    komandalar = Komanda.objects.all()

    for komanda in komandalar:
        komanda_gunler = KomandaGunler.objects.filter(
            komanda = komanda,
            tarix__year = next_m.year,
            tarix__month = next_m.month
        )
        if len(komanda_gunler) != 0:
            continue
        else:
            komanda_gunler = KomandaGunler.objects.create(
                komanda = komanda,
                is_gunleri_count=days_in_month,
                tarix = f"{next_m.year}-{next_m.month}-{1}"
            )
            komanda_gunler.save()
    
    for komanda in komandalar:
        komanda_gunler = KomandaGunler.objects.filter(
            komanda = komanda,
            tarix__year = indi.year,
            tarix__month = indi.month
        )
        if len(komanda_gunler) != 0:
            continue
        else:
            komanda_gunler = KomandaGunler.objects.create(
                komanda = komanda,
                is_gunleri_count=days_in_this_month,
                tarix = f"{indi.year}-{indi.month}-{1}"
            )
            komanda_gunler.save()


# Vezife gunler ---------------------------------------------------
@shared_task(name='work_day_creater_vezife_task1')
def work_day_creater_vezife_task1():
    """
    İş və tətil günlərini create edən task
    """
    indi = datetime.date.today()

    d = pd.to_datetime(f"{indi.year}-{indi.month}-{1}")

    next_m = d + pd.offsets.MonthBegin(1)

    days_in_this_month = pd.Period(f"{indi.year}-{indi.month}-{1}").days_in_month

    days_in_month = pd.Period(f"{next_m.year}-{next_m.month}-{1}").days_in_month

    vezifeler = Vezifeler.objects.all()

    for vezife in vezifeler:
        vezife_gunler = VezifeGunler.objects.filter(
            vezife = vezife,
            tarix__year = next_m.year,
            tarix__month = next_m.month
        )
        if len(vezife_gunler) != 0:
            continue
        else:
            vezife_gunler = VezifeGunler.objects.create(
                vezife = vezife,
                is_gunleri_count=days_in_month,
                tarix = f"{next_m.year}-{next_m.month}-{1}"
            )
            vezife_gunler.save()
    
    for vezife in vezifeler:
        vezife_gunler = VezifeGunler.objects.filter(
            vezife = vezife,
            tarix__year =  indi.year,
            tarix__month = indi.month
        )
        if len(vezife_gunler) != 0:
            continue
        else:
            vezife_gunler = VezifeGunler.objects.create(
                vezife = vezife,
                is_gunleri_count=days_in_this_month,
                tarix = f"{indi.year}-{indi.month}-{1}"
            )
            vezife_gunler.save()



@shared_task(name='work_day_creater_vezife_task15')
def work_day_creater_vezife_task15():
    """
    İş və tətil günlərini create edən task
    """
    indi = datetime.date.today()

    d = pd.to_datetime(f"{indi.year}-{indi.month}-{1}")

    next_m = d + pd.offsets.MonthBegin(1)

    days_in_this_month = pd.Period(f"{indi.year}-{indi.month}-{1}").days_in_month

    days_in_month = pd.Period(f"{next_m.year}-{next_m.month}-{1}").days_in_month

    vezifeler = Vezifeler.objects.all()

    for vezife in vezifeler:
        vezife_gunler = VezifeGunler.objects.filter(
            vezife = vezife,
            tarix__year = next_m.year,
            tarix__month = next_m.month
        )
        if len(vezife_gunler) != 0:
            continue
        else:
            vezife_gunler = VezifeGunler.objects.create(
                vezife = vezife,
                is_gunleri_count=days_in_month,
                tarix = f"{next_m.year}-{next_m.month}-{1}"
            )
            vezife_gunler.save()
    
    for vezife in vezifeler:
        vezife_gunler = VezifeGunler.objects.filter(
            vezife = vezife,
            tarix__year =  indi.year,
            tarix__month = indi.month
        )
        if len(vezife_gunler) != 0:
            continue
        else:
            vezife_gunler = VezifeGunler.objects.create(
                vezife = vezife,
                is_gunleri_count=days_in_this_month,
                tarix = f"{indi.year}-{indi.month}-{1}"
            )
            vezife_gunler.save()