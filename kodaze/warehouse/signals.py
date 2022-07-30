from warehouse.models import Anbar
from company.models import Ofis
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=Ofis)
def create_anbar(sender, instance, created, **kwargs):
    if created:
        ofis = instance
        shirket = ofis.shirket
        ad = f"{ofis.ofis_adi} anbarı"
        anbar = Anbar.objects.filter(ad=ad, ofis=ofis, shirket=shirket)
        if len(anbar) == 0:
            Anbar.objects.create(
                ad=ad,
                ofis=ofis,
                shirket=shirket
            ).save()