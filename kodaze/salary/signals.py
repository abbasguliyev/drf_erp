from django.db.models.signals import post_save
from django.dispatch import receiver

import pandas as pd
import datetime

from account.models import User
from company.models import Vezifeler
from .models import Menecer2Prim, Menecer1PrimNew, MaasGoruntuleme, OfficeLeaderPrim, GroupLeaderPrimNew
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

        group_leader = instance.group_leader
        if group_leader is not None:
            group_leader_status = group_leader.isci_status
        else:
            group_leader_status = None

        menecer1 = instance.menecer1
        if menecer1 is not None:
            menecer1_status = menecer1.isci_status
            menecer1_vezife = menecer1.vezife.vezife_adi
        else:
            menecer1_status = None
            menecer1_vezife = None


        menecer2 = instance.menecer2
        if menecer2 is not None:
            menecer2_status = menecer2.isci_status
            menecer2_vezife = menecer2.vezife.vezife_adi
        else:
            menecer2_status = None
            menecer2_vezife = None

        ofis = instance.ofis
        shirket = instance.shirket
        shobe = instance.group_leader.shobe
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
        # if (group_leader_status is not None):
        #     """
        #     GroupLeaderin kohne uslubla maas hesablanmasi
        #     """
        #     group_leader_prim = GroupLeaderPrim.objects.get(prim_status=group_leader_status, odenis_uslubu=muqavile_odenis_uslubu)
            
        #     group_leader_maas_goruntulenme_bu_ay = MaasGoruntuleme.objects.get(isci=group_leader, tarix=f"{indi.year}-{indi.month}-{1}")
        #     group_leader_maas_goruntulenme_novbeti_ay = MaasGoruntuleme.objects.get(isci=group_leader, tarix=next_m)

        #     group_leader_maas_goruntulenme_bu_ay.satis_sayi = float(group_leader_maas_goruntulenme_bu_ay.satis_sayi) + float(instance.mehsul_sayi)
        #     group_leader_maas_goruntulenme_bu_ay.satis_meblegi = float(group_leader_maas_goruntulenme_bu_ay.satis_meblegi) +  (float(instance.mehsul.qiymet) * float(instance.mehsul_sayi))

        #     group_leader_maas_goruntulenme_bu_ay.save()

        #     group_leader_maas_goruntulenme_novbeti_ay.yekun_maas = float(group_leader_maas_goruntulenme_novbeti_ay.yekun_maas) + (float(group_leader_prim.komandaya_gore_prim) * float(instance.mehsul_sayi))

        #     group_leader_maas_goruntulenme_novbeti_ay.save()
        # --------------------------------------------------------
        if (group_leader_status is not None):
            """
            GroupLeaderin yeni uslubla maas hesablanmasi
            """
            group_leader_prim = GroupLeaderPrimNew.objects.get(prim_status=group_leader_status, vezife=group_leader.vezife)
            
            group_leader_maas_goruntulenme_bu_ay = MaasGoruntuleme.objects.get(isci=group_leader, tarix=f"{indi.year}-{indi.month}-{1}")
            group_leader_maas_goruntulenme_novbeti_ay = MaasGoruntuleme.objects.get(isci=group_leader, tarix=next_m)

            group_leader_maas_goruntulenme_bu_ay.satis_sayi = float(group_leader_maas_goruntulenme_bu_ay.satis_sayi) + float(instance.mehsul_sayi)
            group_leader_maas_goruntulenme_bu_ay.satis_meblegi = float(group_leader_maas_goruntulenme_bu_ay.satis_meblegi) +  (float(instance.mehsul.qiymet) * float(instance.mehsul_sayi))
            
            group_leader_maas_goruntulenme_bu_ay.save()
            if muqavile_odenis_uslubu == "NƏĞD":
                group_leader_maas_goruntulenme_novbeti_ay.yekun_maas = float(group_leader_maas_goruntulenme_novbeti_ay.yekun_maas) + (float(group_leader_prim.negd) * float(instance.mehsul_sayi))
            elif muqavile_odenis_uslubu == "KREDİT":
                if int(muqavile_kredit_muddeti) >= 0 and int(muqavile_kredit_muddeti) <= 3:
                    group_leader_maas_goruntulenme_novbeti_ay.yekun_maas = float(group_leader_maas_goruntulenme_novbeti_ay.yekun_maas) + (float(group_leader_prim.negd) * float(instance.mehsul_sayi))
                elif int(muqavile_kredit_muddeti) >= 4 and int(muqavile_kredit_muddeti) <= 12:
                    group_leader_maas_goruntulenme_novbeti_ay.yekun_maas = float(group_leader_maas_goruntulenme_novbeti_ay.yekun_maas) + (float(group_leader_prim.kredit_4_12) * float(instance.mehsul_sayi))
                elif int(muqavile_kredit_muddeti) >= 13 and int(muqavile_kredit_muddeti) <= 18:
                    group_leader_maas_goruntulenme_novbeti_ay.yekun_maas = float(group_leader_maas_goruntulenme_novbeti_ay.yekun_maas) + (float(group_leader_prim.kredit_13_18) * float(instance.mehsul_sayi))
                elif int(muqavile_kredit_muddeti) >= 19 and int(muqavile_kredit_muddeti) <= 24:
                    group_leader_maas_goruntulenme_novbeti_ay.yekun_maas = float(group_leader_maas_goruntulenme_novbeti_ay.yekun_maas) + (float(group_leader_prim.kredit_19_24) * float(instance.mehsul_sayi))

            group_leader_maas_goruntulenme_novbeti_ay.save()
        # --------------------------------------------------------
        # if (menecer1_vezife == "DEALER"):
        #     menecer1_prim = Menecer1Prim.objects.get(prim_status=menecer1_status, odenis_uslubu=muqavile_odenis_uslubu)

        #     menecer1_maas_goruntulenme_bu_ay = MaasGoruntuleme.objects.get(isci=menecer1, tarix=f"{indi.year}-{indi.month}-{1}")
        #     menecer1_maas_goruntulenme_novbeti_ay = MaasGoruntuleme.objects.get(isci=menecer1, tarix=next_m)

        #     menecer1_maas_goruntulenme_bu_ay.satis_sayi = float(menecer1_maas_goruntulenme_bu_ay.satis_sayi) + float(instance.mehsul_sayi)
        #     menecer1_maas_goruntulenme_bu_ay.satis_meblegi = float(menecer1_maas_goruntulenme_bu_ay.satis_meblegi) +  (float(instance.mehsul.qiymet) * float(instance.mehsul_sayi))

        #     menecer1_maas_goruntulenme_bu_ay.save()


        #     menecer1_maas_goruntulenme_novbeti_ay.yekun_maas = float(menecer1_maas_goruntulenme_novbeti_ay.yekun_maas) + (float(menecer1_prim.komandaya_gore_prim) * float(instance.mehsul_sayi))

        #     menecer1_maas_goruntulenme_novbeti_ay.save()

        # --------------------------------------------------------
        if (menecer1_vezife == "DEALER"):
            """
            Menecer1in yeni uslubla maas hesablanmasi
            """
            menecer1_prim = Menecer1PrimNew.objects.get(prim_status=menecer1_status, vezife=menecer1.vezife)
            
            menecer1_maas_goruntulenme_bu_ay = MaasGoruntuleme.objects.get(isci=menecer1, tarix=f"{indi.year}-{indi.month}-{1}")
            menecer1_maas_goruntulenme_novbeti_ay = MaasGoruntuleme.objects.get(isci=menecer1, tarix=next_m)

            menecer1_maas_goruntulenme_bu_ay.satis_sayi = float(menecer1_maas_goruntulenme_bu_ay.satis_sayi) + float(instance.mehsul_sayi)
            menecer1_maas_goruntulenme_bu_ay.satis_meblegi = float(menecer1_maas_goruntulenme_bu_ay.satis_meblegi) +  (float(instance.mehsul.qiymet) * float(instance.mehsul_sayi))

            menecer1_maas_goruntulenme_bu_ay.save()

            if muqavile_odenis_uslubu == "NƏĞD":
                menecer1_maas_goruntulenme_novbeti_ay.yekun_maas = float(menecer1_maas_goruntulenme_novbeti_ay.yekun_maas) + (float(menecer1_prim.negd) * float(instance.mehsul_sayi))
            elif muqavile_odenis_uslubu == "KREDİT":
                if int(muqavile_kredit_muddeti) >= 0 and int(muqavile_kredit_muddeti) <= 3:
                    menecer1_maas_goruntulenme_novbeti_ay.yekun_maas = float(menecer1_maas_goruntulenme_novbeti_ay.yekun_maas) + (float(menecer1_prim.negd) * float(instance.mehsul_sayi))
                elif int(muqavile_kredit_muddeti) >= 4 and int(muqavile_kredit_muddeti) <= 12:
                    menecer1_maas_goruntulenme_novbeti_ay.yekun_maas = float(menecer1_maas_goruntulenme_novbeti_ay.yekun_maas) + (float(menecer1_prim.kredit_4_12) * float(instance.mehsul_sayi))
                elif int(muqavile_kredit_muddeti) >= 13 and int(muqavile_kredit_muddeti) <= 18:
                    menecer1_maas_goruntulenme_novbeti_ay.yekun_maas = float(menecer1_maas_goruntulenme_novbeti_ay.yekun_maas) + (float(menecer1_prim.kredit_13_18) * float(instance.mehsul_sayi))
                elif int(muqavile_kredit_muddeti) >= 19 and int(muqavile_kredit_muddeti) <= 24:
                    menecer1_maas_goruntulenme_novbeti_ay.yekun_maas = float(menecer1_maas_goruntulenme_novbeti_ay.yekun_maas) + (float(menecer1_prim.kredit_19_24) * float(instance.mehsul_sayi))
            menecer1_maas_goruntulenme_novbeti_ay.save()

        # --------------------------------------------------------
        if (menecer2_vezife == "CANVASSER"):
            menecer2_prim = Menecer2Prim.objects.get(prim_status=menecer2_status, vezife=menecer2.vezife)

            menecer2_maas_goruntulenme_bu_ay = MaasGoruntuleme.objects.get(isci=menecer2, tarix=f"{indi.year}-{indi.month}-{1}")
            menecer2_maas_goruntulenme_novbeti_ay = MaasGoruntuleme.objects.get(isci=menecer2, tarix=next_m)

            menecer2_maas_goruntulenme_bu_ay.satis_sayi = float(menecer2_maas_goruntulenme_bu_ay.satis_sayi) + float(instance.mehsul_sayi)
            menecer2_maas_goruntulenme_bu_ay.satis_meblegi = float(menecer2_maas_goruntulenme_bu_ay.satis_meblegi) +  (float(instance.mehsul.qiymet) * float(instance.mehsul_sayi))
            menecer2_maas_goruntulenme_bu_ay.save()

            satis_sayina_gore_prim = 0
            
            if (menecer2_maas_goruntulenme_bu_ay.satis_sayi >= 9) and (menecer2_maas_goruntulenme_bu_ay.satis_sayi <= 14):
                satis_sayina_gore_prim = menecer2_prim.satis9_14
            elif (menecer2_maas_goruntulenme_bu_ay.satis_sayi >= 15):
                satis_sayina_gore_prim = menecer2_prim.satis15p
            elif (menecer2_maas_goruntulenme_bu_ay.satis_sayi >= 20):
                satis_sayina_gore_prim = menecer2_prim.satis20p

            menecer2_maas_goruntulenme_novbeti_ay.yekun_maas = float(menecer2_maas_goruntulenme_novbeti_ay.yekun_maas) + (float(menecer2_prim.komandaya_gore_prim) * float(instance.mehsul_sayi)) + float(satis_sayina_gore_prim)

            menecer2_maas_goruntulenme_novbeti_ay.save()

        
        menecer2Vezife = Vezifeler.objects.get(vezife_adi__icontains="CANVASSER", shirket=shirket)
        menecer2s = User.objects.filter(ofis=ofis, vezife=menecer2Vezife)

        for menecer2 in menecer2s:
            menecer2_status = menecer2.isci_status
            menecer2_prim = Menecer2Prim.objects.get(prim_status=menecer2_status, vezife=menecer2.vezife)

            menecer2_maas_goruntulenme_novbeti_ay = MaasGoruntuleme.objects.get(isci=menecer2, tarix=next_m)

            menecer2_maas_goruntulenme_novbeti_ay.yekun_maas = float(menecer2_maas_goruntulenme_novbeti_ay.yekun_maas) + (float(menecer2_prim.ofise_gore_prim) * float(instance.mehsul_sayi))

            menecer2_maas_goruntulenme_novbeti_ay.save()