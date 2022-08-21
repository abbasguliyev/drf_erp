import datetime
from company.models import Vezifeler
from .models import User
from celery import shared_task
import pandas as pd
from salary.models import CanvasserPrim, MaasGoruntuleme, OfficeLeaderPrim, VanLeaderPrim



@shared_task(name='maas_goruntuleme_create_task')
def maas_goruntuleme_create_task():
    users = User.objects.all()
    indi = datetime.date.today()
    
    d = pd.to_datetime(f"{indi.year}-{indi.month}-{1}")

    next_m = d + pd.offsets.MonthBegin(1)

    for user in users:
        isci_maas = MaasGoruntuleme.objects.filter(
            isci=user, 
            tarix__year = next_m.year,
            tarix__month = next_m.month
        )
        if len(isci_maas) != 0:
            continue
        else:
            if user.maas_uslubu == "FİX": 
                MaasGoruntuleme.objects.create(isci=user, tarix=f"{next_m.year}-{next_m.month}-{1}", yekun_maas=user.maas).save()
            else:    
                MaasGoruntuleme.objects.create(isci=user, tarix=f"{next_m.year}-{next_m.month}-{1}").save()

    for user in users:
        isci_maas = MaasGoruntuleme.objects.filter(
            isci=user, 
            tarix__year = indi.year,
            tarix__month = indi.month
        )
        if len(isci_maas) != 0:
            continue
        else:
            if user.maas_uslubu == "FİX": 
                MaasGoruntuleme.objects.create(isci=user, tarix=f"{indi.year}-{indi.month}-{1}", yekun_maas=user.maas).save()
            else:    
                MaasGoruntuleme.objects.create(isci=user, tarix=f"{indi.year}-{indi.month}-{1}").save()

@shared_task(name='maas_goruntuleme_create_task_15')
def maas_goruntuleme_create_task_15():
    users = User.objects.all()
    indi = datetime.date.today()
    
    d = pd.to_datetime(f"{indi.year}-{indi.month}-{1}")

    next_m = d + pd.offsets.MonthBegin(1)

    for user in users:
        isci_maas = MaasGoruntuleme.objects.filter(
            isci=user, 
            tarix__year = next_m.year,
            tarix__month = next_m.month
        )
        if len(isci_maas) != 0:
            continue
        else:
            if user.maas_uslubu == "FİX": 
                MaasGoruntuleme.objects.create(isci=user, tarix=f"{next_m.year}-{next_m.month}-{1}", yekun_maas=user.maas).save()
            else:    
                MaasGoruntuleme.objects.create(isci=user, tarix=f"{next_m.year}-{next_m.month}-{1}").save()

    for user in users:
        isci_maas = MaasGoruntuleme.objects.filter(
            isci=user, 
            tarix__year = indi.year,
            tarix__month = indi.month
        )
        if len(isci_maas) != 0:
            continue
        else:
            if user.maas_uslubu == "FİX": 
                MaasGoruntuleme.objects.create(isci=user, tarix=f"{indi.year}-{indi.month}-{1}", yekun_maas=user.maas).save()
            else:    
                MaasGoruntuleme.objects.create(isci=user, tarix=f"{indi.year}-{indi.month}-{1}").save()


@shared_task(name='isci_fix_maas_auto_elave_et')
def isci_fix_maas_auto_elave_et():
    indi = datetime.date.today()

    bu_ay = f"{indi.year}-{indi.month}-{1}"
    
    d = pd.to_datetime(f"{indi.year}-{indi.month}-{1}")

    evvelki_ay = d - pd.offsets.MonthBegin(1)

    officeLeaderVezife = Vezifeler.objects.filter(vezife_adi="OFFICE LEADER")[0]
    officeLeaders = User.objects.filter(vezife__vezife_adi=officeLeaderVezife.vezife_adi)

    for officeLeader in officeLeaders:
        officeLeader_status = officeLeader.isci_status

        ofisleader_prim = OfficeLeaderPrim.objects.get(prim_status=officeLeader_status, vezife=officeLeader.vezife)
        print(f"************{officeLeader.id=}")
        officeLeader_maas_goruntulenme_bu_ay = MaasGoruntuleme.objects.get(isci=officeLeader, tarix=bu_ay)

        officeLeader_maas_goruntulenme_bu_ay.yekun_maas = float(officeLeader_maas_goruntulenme_bu_ay.yekun_maas) + float(ofisleader_prim.fix_maas)
        officeLeader_maas_goruntulenme_bu_ay.save()
    
    # vanLeaderVezife = Vezifeler.objects.get(vezife_adi="VAN LEADER")
    # vanLeaders = User.objects.filter(vezife=vanLeaderVezife)

    # for vanleader in vanLeaders:
    #     vanleader_status = vanleader.isci_status

    #     vanleader_prim = VanLeaderPrim.objects.get(prim_status=vanleader_status, odenis_uslubu="NƏĞD")

    #     vanleader_maas_goruntulenme_bu_ay = MaasGoruntuleme.objects.get(isci=vanleader, tarix=bu_ay)

    #     vanleader_maas_goruntulenme_bu_ay.yekun_maas = float(vanleader_maas_goruntulenme_bu_ay.yekun_maas) + float(vanleader_prim.fix_maas)
    #     vanleader_maas_goruntulenme_bu_ay.save()

    canvasserVezife = Vezifeler.objects.filter(vezife_adi="CANVASSER")[0]
    canvassers = User.objects.filter(vezife__vezife_adi=canvasserVezife.vezife_adi)

    for canvesser in canvassers:
        canvesser_status = canvesser.isci_status

        canvesser_prim = CanvasserPrim.objects.get(prim_status=canvesser_status, vezife=canvesser.vezife)

        canvesser_maas_goruntulenme_evvelki_ay = MaasGoruntuleme.objects.get(isci=canvesser, tarix=evvelki_ay)
        canvesser_maas_goruntulenme_bu_ay = MaasGoruntuleme.objects.get(isci=canvesser, tarix=f"{indi.year}-{indi.month}-{1}")

        satis_sayina_gore_prim = 0
        if (canvesser_maas_goruntulenme_evvelki_ay.satis_sayi == 0):
            satis_sayina_gore_prim = canvesser_prim.satis0
        elif (canvesser_maas_goruntulenme_evvelki_ay.satis_sayi >= 1) and (canvesser_maas_goruntulenme_evvelki_ay.satis_sayi <= 8):
            satis_sayina_gore_prim = canvesser_prim.satis1_8

        canvesser_maas_goruntulenme_bu_ay.yekun_maas = float(canvesser_maas_goruntulenme_bu_ay.yekun_maas) + float(satis_sayina_gore_prim) + float(canvesser_prim.fix_maas)
        canvesser_maas_goruntulenme_bu_ay.save()
        canvesser_maas_goruntulenme_evvelki_ay.save()