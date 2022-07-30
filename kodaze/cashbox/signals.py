from company.models import Holding, Ofis, Shirket
from .models import HoldingKassa, OfisKassa, ShirketKassa
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=Ofis)
def create_ofis_kassa(sender, instance, created, **kwargs):
    if created:
        ofis_kassa = OfisKassa.objects.filter(ofis=instance)
        if len(ofis_kassa) == 0:
            ofis = instance
            balans = 0
            ofis_kassa = OfisKassa.objects.create(ofis=ofis, balans=balans).save()

@receiver(post_save, sender=Shirket)
def create_shirket_kassa(sender, instance, created, **kwargs):
    if created:
        shirket_kassa = ShirketKassa.objects.filter(shirket=instance)
        if len(shirket_kassa) == 0:
            shirket = instance
            balans = 0
            shirket_kassa = ShirketKassa.objects.create(shirket=shirket, balans=balans).save()

@receiver(post_save, sender=Holding)
def create_holding_kassa(sender, instance, created, **kwargs):
    if created:
        holding_kassa = HoldingKassa.objects.filter(holding=instance)
        if len(holding_kassa) == 0:
            holding = instance
            balans = 0
            holding_kassa = HoldingKassa.objects.create(holding=holding, balans=balans).save()
