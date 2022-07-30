from django.db.models.signals import post_save
from django.dispatch import receiver

import pandas as pd
import datetime

from account.models import User
from company.models import Vezifeler
from .models import CanvasserPrim, DealerPrimNew, MaasGoruntuleme, OfficeLeaderPrim, VanLeaderPrimNew
from contract.models import Muqavile
import traceback

@receiver(post_save, sender=Muqavile)
def create_prim(sender, instance, created, **kwargs):
    if created:
        indi = datetime.date.today()
        d = pd.to_datetime(f"{indi.year}-{indi.month}-{1}")
        next_m = d + pd.offsets.MonthBegin(1)
        print(f"{indi=}")
        print(f"{next_m=}")
        days_in_mont = pd.Period(f"{next_m.year}-{next_m.month}-{1}").days_in_month
        
        muqavile_kredit_muddeti = instance.kredit_muddeti
        muqavile_odenis_uslubu = instance.odenis_uslubu
        if muqavile_odenis_uslubu == "İKİ DƏFƏYƏ NƏĞD":
            muqavile_odenis_uslubu = "NƏĞD"

        vanleader = instance.vanleader
        if vanleader is not None:
            vanleader_status = vanleader.isci_status
        else:
            vanleader_status = None

        dealer = instance.dealer
        if dealer is not None:
            dealer_status = dealer.isci_status
            dealer_vezife = dealer.vezife.vezife_adi
        else:
            dealer_status = None
            dealer_vezife = None


        canvesser = instance.canvesser
        if canvesser is not None:
            canvesser_status = canvesser.isci_status
            canvesser_vezife = canvesser.vezife.vezife_adi
        else:
            canvesser_status = None
            canvesser_vezife = None

        ofis = instance.ofis
        shirket = instance.shirket
        shobe = instance.vanleader.shobe
        print(f"{shirket=}")
        print(f"{shobe=}")
        if (ofis is not None) or (ofis != ""):
            officeLeaderVezife = Vezifeler.objects.get(vezife_adi__icontains="OFFICE LEADER", shirket=shirket)
            officeLeaders = User.objects.filter(ofis=ofis, vezife=officeLeaderVezife)

            for officeLeader in officeLeaders:
                officeLeader_status = officeLeader.isci_status
                ofisleader_prim = OfficeLeaderPrim.objects.get(prim_status=officeLeader_status, vezife=officeLeaderVezife)

                officeLeader_maas_goruntulenme_bu_ay = MaasGoruntuleme.objects.get(isci=officeLeader, tarix=f"{indi.year}-{indi.month}-{1}")
                officeLeader_maas_goruntulenme_novbeti_ay = MaasGoruntuleme.objects.get(isci=officeLeader, tarix=f"{next_m.year}-{next_m.month}-{1}")

                officeLeader_maas_goruntulenme_bu_ay.satis_sayi = float(officeLeader_maas_goruntulenme_bu_ay.satis_sayi) + float(instance.mehsul_sayi)
                officeLeader_maas_goruntulenme_bu_ay.satis_meblegi = float(officeLeader_maas_goruntulenme_bu_ay.satis_meblegi) + (float(instance.mehsul.qiymet) * float(instance.mehsul_sayi))
                officeLeader_maas_goruntulenme_bu_ay.save()

                officeLeader_maas_goruntulenme_novbeti_ay.yekun_maas = float(officeLeader_maas_goruntulenme_novbeti_ay.yekun_maas) + (float(ofisleader_prim.ofise_gore_prim) * float(instance.mehsul_sayi))
                officeLeader_maas_goruntulenme_novbeti_ay.save()

        # --------------------------------------------------------
        # if (vanleader_status is not None):
        #     """
        #     Vanleaderin kohne uslubla maas hesablanmasi
        #     """
        #     vanleader_prim = VanLeaderPrim.objects.get(prim_status=vanleader_status, odenis_uslubu=muqavile_odenis_uslubu)
            
        #     vanleader_maas_goruntulenme_bu_ay = MaasGoruntuleme.objects.get(isci=vanleader, tarix=f"{indi.year}-{indi.month}-{1}")
        #     vanleader_maas_goruntulenme_novbeti_ay = MaasGoruntuleme.objects.get(isci=vanleader, tarix=next_m)

        #     vanleader_maas_goruntulenme_bu_ay.satis_sayi = float(vanleader_maas_goruntulenme_bu_ay.satis_sayi) + float(instance.mehsul_sayi)
        #     vanleader_maas_goruntulenme_bu_ay.satis_meblegi = float(vanleader_maas_goruntulenme_bu_ay.satis_meblegi) +  (float(instance.mehsul.qiymet) * float(instance.mehsul_sayi))

        #     vanleader_maas_goruntulenme_bu_ay.save()

        #     vanleader_maas_goruntulenme_novbeti_ay.yekun_maas = float(vanleader_maas_goruntulenme_novbeti_ay.yekun_maas) + (float(vanleader_prim.komandaya_gore_prim) * float(instance.mehsul_sayi))

        #     vanleader_maas_goruntulenme_novbeti_ay.save()
        # --------------------------------------------------------
        if (vanleader_status is not None):
            """
            Vanleaderin yeni uslubla maas hesablanmasi
            """
            vanleader_prim = VanLeaderPrimNew.objects.get(prim_status=vanleader_status, vezife=vanleader.vezife)
            
            vanleader_maas_goruntulenme_bu_ay = MaasGoruntuleme.objects.get(isci=vanleader, tarix=f"{indi.year}-{indi.month}-{1}")
            vanleader_maas_goruntulenme_novbeti_ay = MaasGoruntuleme.objects.get(isci=vanleader, tarix=next_m)

            vanleader_maas_goruntulenme_bu_ay.satis_sayi = float(vanleader_maas_goruntulenme_bu_ay.satis_sayi) + float(instance.mehsul_sayi)
            vanleader_maas_goruntulenme_bu_ay.satis_meblegi = float(vanleader_maas_goruntulenme_bu_ay.satis_meblegi) +  (float(instance.mehsul.qiymet) * float(instance.mehsul_sayi))
            
            vanleader_maas_goruntulenme_bu_ay.save()
            if muqavile_odenis_uslubu == "NƏĞD":
                vanleader_maas_goruntulenme_novbeti_ay.yekun_maas = float(vanleader_maas_goruntulenme_novbeti_ay.yekun_maas) + (float(vanleader_prim.negd) * float(instance.mehsul_sayi))
            elif muqavile_odenis_uslubu == "KREDİT":
                if int(muqavile_kredit_muddeti) >= 0 and int(muqavile_kredit_muddeti) <= 3:
                    vanleader_maas_goruntulenme_novbeti_ay.yekun_maas = float(vanleader_maas_goruntulenme_novbeti_ay.yekun_maas) + (float(vanleader_prim.negd) * float(instance.mehsul_sayi))
                elif int(muqavile_kredit_muddeti) >= 4 and int(muqavile_kredit_muddeti) <= 12:
                    vanleader_maas_goruntulenme_novbeti_ay.yekun_maas = float(vanleader_maas_goruntulenme_novbeti_ay.yekun_maas) + (float(vanleader_prim.kredit_4_12) * float(instance.mehsul_sayi))
                elif int(muqavile_kredit_muddeti) >= 13 and int(muqavile_kredit_muddeti) <= 18:
                    vanleader_maas_goruntulenme_novbeti_ay.yekun_maas = float(vanleader_maas_goruntulenme_novbeti_ay.yekun_maas) + (float(vanleader_prim.kredit_13_18) * float(instance.mehsul_sayi))
                elif int(muqavile_kredit_muddeti) >= 19 and int(muqavile_kredit_muddeti) <= 24:
                    vanleader_maas_goruntulenme_novbeti_ay.yekun_maas = float(vanleader_maas_goruntulenme_novbeti_ay.yekun_maas) + (float(vanleader_prim.kredit_19_24) * float(instance.mehsul_sayi))

            vanleader_maas_goruntulenme_novbeti_ay.save()
        # --------------------------------------------------------
        # if (dealer_vezife == "DEALER"):
        #     dealer_prim = DealerPrim.objects.get(prim_status=dealer_status, odenis_uslubu=muqavile_odenis_uslubu)

        #     dealer_maas_goruntulenme_bu_ay = MaasGoruntuleme.objects.get(isci=dealer, tarix=f"{indi.year}-{indi.month}-{1}")
        #     dealer_maas_goruntulenme_novbeti_ay = MaasGoruntuleme.objects.get(isci=dealer, tarix=next_m)

        #     dealer_maas_goruntulenme_bu_ay.satis_sayi = float(dealer_maas_goruntulenme_bu_ay.satis_sayi) + float(instance.mehsul_sayi)
        #     dealer_maas_goruntulenme_bu_ay.satis_meblegi = float(dealer_maas_goruntulenme_bu_ay.satis_meblegi) +  (float(instance.mehsul.qiymet) * float(instance.mehsul_sayi))

        #     dealer_maas_goruntulenme_bu_ay.save()


        #     dealer_maas_goruntulenme_novbeti_ay.yekun_maas = float(dealer_maas_goruntulenme_novbeti_ay.yekun_maas) + (float(dealer_prim.komandaya_gore_prim) * float(instance.mehsul_sayi))

        #     dealer_maas_goruntulenme_novbeti_ay.save()

        # --------------------------------------------------------
        if (dealer_vezife == "DEALER"):
            """
            Dealerin yeni uslubla maas hesablanmasi
            """
            dealer_prim = DealerPrimNew.objects.get(prim_status=dealer_status, vezife=dealer.vezife)
            
            dealer_maas_goruntulenme_bu_ay = MaasGoruntuleme.objects.get(isci=dealer, tarix=f"{indi.year}-{indi.month}-{1}")
            dealer_maas_goruntulenme_novbeti_ay = MaasGoruntuleme.objects.get(isci=dealer, tarix=next_m)

            dealer_maas_goruntulenme_bu_ay.satis_sayi = float(dealer_maas_goruntulenme_bu_ay.satis_sayi) + float(instance.mehsul_sayi)
            dealer_maas_goruntulenme_bu_ay.satis_meblegi = float(dealer_maas_goruntulenme_bu_ay.satis_meblegi) +  (float(instance.mehsul.qiymet) * float(instance.mehsul_sayi))

            dealer_maas_goruntulenme_bu_ay.save()

            if muqavile_odenis_uslubu == "NƏĞD":
                dealer_maas_goruntulenme_novbeti_ay.yekun_maas = float(dealer_maas_goruntulenme_novbeti_ay.yekun_maas) + (float(dealer_prim.negd) * float(instance.mehsul_sayi))
            elif muqavile_odenis_uslubu == "KREDİT":
                if int(muqavile_kredit_muddeti) >= 0 and int(muqavile_kredit_muddeti) <= 3:
                    dealer_maas_goruntulenme_novbeti_ay.yekun_maas = float(dealer_maas_goruntulenme_novbeti_ay.yekun_maas) + (float(dealer_prim.negd) * float(instance.mehsul_sayi))
                elif int(muqavile_kredit_muddeti) >= 4 and int(muqavile_kredit_muddeti) <= 12:
                    dealer_maas_goruntulenme_novbeti_ay.yekun_maas = float(dealer_maas_goruntulenme_novbeti_ay.yekun_maas) + (float(dealer_prim.kredit_4_12) * float(instance.mehsul_sayi))
                elif int(muqavile_kredit_muddeti) >= 13 and int(muqavile_kredit_muddeti) <= 18:
                    dealer_maas_goruntulenme_novbeti_ay.yekun_maas = float(dealer_maas_goruntulenme_novbeti_ay.yekun_maas) + (float(dealer_prim.kredit_13_18) * float(instance.mehsul_sayi))
                elif int(muqavile_kredit_muddeti) >= 19 and int(muqavile_kredit_muddeti) <= 24:
                    dealer_maas_goruntulenme_novbeti_ay.yekun_maas = float(dealer_maas_goruntulenme_novbeti_ay.yekun_maas) + (float(dealer_prim.kredit_19_24) * float(instance.mehsul_sayi))
            dealer_maas_goruntulenme_novbeti_ay.save()

        # --------------------------------------------------------
        if (canvesser_vezife == "CANVASSER"):
            canvesser_prim = CanvasserPrim.objects.get(prim_status=canvesser_status, vezife=canvesser.vezife)

            canvesser_maas_goruntulenme_bu_ay = MaasGoruntuleme.objects.get(isci=canvesser, tarix=f"{indi.year}-{indi.month}-{1}")
            canvesser_maas_goruntulenme_novbeti_ay = MaasGoruntuleme.objects.get(isci=canvesser, tarix=next_m)

            canvesser_maas_goruntulenme_bu_ay.satis_sayi = float(canvesser_maas_goruntulenme_bu_ay.satis_sayi) + float(instance.mehsul_sayi)
            canvesser_maas_goruntulenme_bu_ay.satis_meblegi = float(canvesser_maas_goruntulenme_bu_ay.satis_meblegi) +  (float(instance.mehsul.qiymet) * float(instance.mehsul_sayi))
            canvesser_maas_goruntulenme_bu_ay.save()

            satis_sayina_gore_prim = 0
            
            if (canvesser_maas_goruntulenme_bu_ay.satis_sayi >= 9) and (canvesser_maas_goruntulenme_bu_ay.satis_sayi <= 14):
                satis_sayina_gore_prim = canvesser_prim.satis9_14
            elif (canvesser_maas_goruntulenme_bu_ay.satis_sayi >= 15):
                satis_sayina_gore_prim = canvesser_prim.satis15p
            elif (canvesser_maas_goruntulenme_bu_ay.satis_sayi >= 20):
                satis_sayina_gore_prim = canvesser_prim.satis20p

            canvesser_maas_goruntulenme_novbeti_ay.yekun_maas = float(canvesser_maas_goruntulenme_novbeti_ay.yekun_maas) + (float(canvesser_prim.komandaya_gore_prim) * float(instance.mehsul_sayi)) + float(satis_sayina_gore_prim)

            canvesser_maas_goruntulenme_novbeti_ay.save()

        
        canvesserVezife = Vezifeler.objects.get(vezife_adi__icontains="CANVASSER", shirket=shirket)
        canvessers = User.objects.filter(ofis=ofis, vezife=canvesserVezife)

        for canvesser in canvessers:
            canvesser_status = canvesser.isci_status
            canvesser_prim = CanvasserPrim.objects.get(prim_status=canvesser_status, vezife=canvesser.vezife)

            canvesser_maas_goruntulenme_novbeti_ay = MaasGoruntuleme.objects.get(isci=canvesser, tarix=next_m)

            canvesser_maas_goruntulenme_novbeti_ay.yekun_maas = float(canvesser_maas_goruntulenme_novbeti_ay.yekun_maas) + (float(canvesser_prim.ofise_gore_prim) * float(instance.mehsul_sayi))

            canvesser_maas_goruntulenme_novbeti_ay.save()