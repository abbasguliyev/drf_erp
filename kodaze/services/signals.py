from contract.models import Muqavile
from . models import Servis, ServisOdeme
from django.db.models.signals import post_save
from django.dispatch import receiver
import datetime
import pandas as pd

from .tasks import create_services_task

@receiver(post_save, sender=Muqavile)
def create_services(sender, instance, created, **kwargs):
    if created:
        create_services_task.delay(instance.id)

@receiver(post_save, sender=Servis)
def create_servis_odeme(sender, instance, created, **kwargs):
    if created:
        kredit_muddeti = instance.kredit_muddeti
        kredit = instance.kredit
        if int(kredit_muddeti) == 0:
            kredit_muddeti = 1
        print(f"****************************{kredit_muddeti=}")
        print(f"****************************{kredit=}")
        endirim = instance.endirim
        if endirim == None:
            endirim = 0
        
        ilkin_odenis = instance.ilkin_odenis
        if ilkin_odenis == None:
            ilkin_odenis = 0

        servis_qiymeti = instance.servis_qiymeti
        yekun = float(servis_qiymeti) - float(ilkin_odenis) - float(endirim)
        netice1 = yekun // kredit_muddeti
        netice2 = netice1 * (kredit_muddeti - 1)
        son_ay = yekun - netice2
        # indi_d = servis_tarixi
        # indi = f"{indi_d.year}-{indi_d.month}-{1}"
        
        indi_d = instance.create_date
        servis_tarixi_str = instance.servis_tarix
        print(f"{servis_tarixi_str=}")

        # servis_tarixi = pd.to_datetime(f"{servis_tarixi_str.year}-{servis_tarixi_str.month}-{servis_tarixi_str.day}")
        try:
            servis_tarixi = datetime.datetime.strptime(f"{servis_tarixi_str.year}-{servis_tarixi_str.month}-{servis_tarixi_str.day}", '%d-%m-%Y')
        except:
            servis_tarixi = datetime.datetime.strptime(servis_tarixi_str, '%d-%m-%Y')
        inc_month = pd.date_range(servis_tarixi, periods=kredit_muddeti+1, freq='M')

        if kredit == False:
            servis_odeme = ServisOdeme.objects.create(
                                servis = instance,
                                odenilecek_umumi_mebleg=yekun,
                                odenilecek_mebleg=son_ay,
                                odeme_tarix=f"{servis_tarixi.year}-{servis_tarixi.month}-{servis_tarixi.day}"
                            ).save()
        elif kredit == True:
            j = 1
            while(j<=int(kredit_muddeti)):
                if(j == int(kredit_muddeti)):
                    if(servis_tarixi.day < 29):
                        servis_odeme = ServisOdeme.objects.create(
                            servis = instance,
                            odenilecek_umumi_mebleg=yekun,
                            odenilecek_mebleg=son_ay,
                            odeme_tarix=f"{inc_month[j].year}-{inc_month[j].month}-{servis_tarixi.day}"
                        ).save()
                    elif(servis_tarixi.day == 31 or servis_tarixi.day == 30 or servis_tarixi.day == 29):
                        if(inc_month[j].day <= servis_tarixi.day):
                            servis_odeme = ServisOdeme.objects.create(
                                servis = instance,
                                odenilecek_umumi_mebleg=yekun,
                                odenilecek_mebleg=son_ay,
                                odeme_tarix=f"{inc_month[j].year}-{inc_month[j].month}-{inc_month[j].day}"
                            ).save()
                        elif(inc_month[j].day > servis_tarixi.day):
                            servis_odeme = ServisOdeme.objects.create(
                                servis = instance,
                                odenilecek_umumi_mebleg=yekun,
                                odenilecek_mebleg=son_ay,
                                odeme_tarix=f"{inc_month[j].year}-{inc_month[j].month}-{servis_tarixi.day}"
                            ).save()
                else:
                    if(servis_tarixi.day < 29):
                        servis_odeme = ServisOdeme.objects.create(
                            servis = instance,
                            odenilecek_umumi_mebleg=yekun,
                            odenilecek_mebleg=netice1,
                            odeme_tarix=f"{inc_month[j].year}-{inc_month[j].month}-{servis_tarixi.day}"
                        ).save()
                    elif(servis_tarixi.day == 31 or servis_tarixi.day == 30 or servis_tarixi.day == 29):
                        if(inc_month[j].day <= servis_tarixi.day):
                            servis_odeme = ServisOdeme.objects.create(
                                servis = instance,
                                odenilecek_umumi_mebleg=yekun,
                                odenilecek_mebleg=netice1,
                                odeme_tarix=f"{inc_month[j].year}-{inc_month[j].month}-{inc_month[j].day}"
                            ).save()
                        elif(inc_month[j].day > servis_tarixi.day):
                            servis_odeme = ServisOdeme.objects.create(
                                servis = instance,
                                odenilecek_umumi_mebleg=yekun,
                                odenilecek_mebleg=netice1,
                                odeme_tarix=f"{inc_month[j].year}-{inc_month[j].month}-{servis_tarixi.day}"
                            ).save()
                j += 1
