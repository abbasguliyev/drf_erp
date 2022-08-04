from .models import Muqavile
from django.db.models.signals import post_save
from django.dispatch import receiver

from .tasks import create_odeme_tarix_task, demo_satis_sayi_task

from restAPI.v1.utils.ocean_muqavile_pdf_create import (
    okean_create_muqavile_pdf, 
    okean_muqavile_pdf_canvas, 
    ocean_kredit_create_muqavile_pdf,
    ocean_kredit_muqavile_pdf_canvas
)

from restAPI.v1.utils.magnus_muqavile_pdf_create import (
    magnus_create_muqavile_pdf,
    magnus_muqavile_pdf_canvas,
    magnus_kredit_create_muqavile_pdf,
    magnus_kredit_muqavile_pdf_canvas
)

@receiver(post_save, sender=Muqavile)
def create_odeme_tarix(sender, instance, created, **kwargs):
    if created:
        create_odeme_tarix_task.delay(instance.id, True)

@receiver(post_save, sender=Muqavile)
def create_and_add_pdf_to_muqavile(sender, instance, created, **kwargs):
    if created:
        print("Signal işə düşdü")
        
        okean = "OCEAN"
        magnus = "MAGNUS"

        if instance.ofis.shirket.shirket_adi == okean:
            muqavile_pdf_canvas_list = okean_muqavile_pdf_canvas(
                muqavile=instance, musteri=instance.musteri
            )
            muqavile_pdf = okean_create_muqavile_pdf(muqavile_pdf_canvas_list, instance)
        elif instance.ofis.shirket.shirket_adi == magnus:
            muqavile_pdf_canvas_list = magnus_muqavile_pdf_canvas(
                muqavile=instance, musteri=instance.musteri
            )
            muqavile_pdf = magnus_create_muqavile_pdf(muqavile_pdf_canvas_list, instance)
        
        instance.pdf = muqavile_pdf
        instance.save()
    
@receiver(post_save, sender=Muqavile)
def create_and_add_pdf_to_muqavile_kredit(sender, instance, created, **kwargs):
    if created:
        print("Signal işə düşdü")

        okean = "OCEAN"
        magnus = "MAGNUS"

        if instance.ofis.shirket.shirket_adi == okean:
            muqavile_pdf_canvas_list = ocean_kredit_muqavile_pdf_canvas(
                muqavile=instance
            )
            muqavile_pdf = ocean_kredit_create_muqavile_pdf(muqavile_pdf_canvas_list, instance)
        elif instance.ofis.shirket.shirket_adi == magnus:
            muqavile_pdf_canvas_list = magnus_kredit_muqavile_pdf_canvas(
                muqavile=instance
            )
            muqavile_pdf = magnus_kredit_create_muqavile_pdf(muqavile_pdf_canvas_list, instance)
        instance.pdf_elave = muqavile_pdf
        instance.save()


@receiver(post_save, sender=Muqavile)
def demo_satis_sayi(sender, instance, created, **kwargs):
    if created:
        demo_satis_sayi_task.delay(instance.id)