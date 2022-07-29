from django.db import models

from django.contrib.auth import get_user_model

USER = get_user_model()

# Create your models here.

class OfisdenShirketeTransfer(models.Model):
    transfer_eden = models.ForeignKey(USER, on_delete=models.CASCADE, null=True,
                                      related_name="user_ofis_shirket_transfer")
    ofis_kassa = models.ForeignKey("cashbox.OfisKassa", on_delete=models.CASCADE, null=True,
                                   related_name="ofisden_shirkete_transfer")
    shirket_kassa = models.ForeignKey("cashbox.ShirketKassa", on_delete=models.CASCADE, null=True,
                                      related_name="ofisden_shirkete_transfer")
    transfer_meblegi = models.FloatField(default=0)
    transfer_tarixi = models.DateField(auto_now=True)
    transfer_qeydi = models.TextField(null=True, blank=True)
    qalan_mebleg = models.FloatField(default=0, blank=True)
    evvelki_balans = models.FloatField(default=0, blank=True)
    sonraki_balans = models.FloatField(default=0, blank=True)

    class Meta:
        ordering = ("-pk",)

    def __str__(self) -> str:
        return f"{self.ofis_kassa} -> {self.shirket_kassa} {self.transfer_meblegi} azn"


class ShirketdenOfislereTransfer(models.Model):
    transfer_eden = models.ForeignKey(USER, on_delete=models.CASCADE, null=True,
                                      related_name="user_shirket_ofis_transfer")
    shirket_kassa = models.ForeignKey("cashbox.ShirketKassa", on_delete=models.CASCADE, null=True,
                                      related_name="shirketden_ofise_transfer")
    ofis_kassa = models.ManyToManyField("cashbox.OfisKassa", related_name="shirketden_ofise_transfer")
    transfer_meblegi = models.FloatField(default=0)
    transfer_tarixi = models.DateField(auto_now=True)
    transfer_qeydi = models.TextField(null=True, blank=True)
    qalan_mebleg = models.FloatField(default=0, blank=True)
    evvelki_balans = models.FloatField(default=0, blank=True)
    sonraki_balans = models.FloatField(default=0, blank=True)

    class Meta:
        ordering = ("-pk",)

    def __str__(self) -> str:
        return f"{self.shirket_kassa} -> {self.ofis_kassa} {self.transfer_meblegi} azn"


class ShirketdenHoldingeTransfer(models.Model):
    transfer_eden = models.ForeignKey(USER, on_delete=models.CASCADE, null=True,
                                      related_name="user_shirket_holding_transfer")
    shirket_kassa = models.ForeignKey("cashbox.ShirketKassa", on_delete=models.CASCADE, null=True,
                                      related_name="shirketden_holdinge_transfer")
    holding_kassa = models.ForeignKey("cashbox.HoldingKassa", on_delete=models.CASCADE, null=True,
                                      related_name="shirketden_holdinge_transfer")
    transfer_meblegi = models.FloatField(default=0)
    transfer_tarixi = models.DateField(auto_now=True)
    transfer_qeydi = models.TextField(null=True, blank=True)
    qalan_mebleg = models.FloatField(default=0, blank=True)
    evvelki_balans = models.FloatField(default=0, blank=True)
    sonraki_balans = models.FloatField(default=0, blank=True)

    class Meta:
        ordering = ("-pk",)

    def __str__(self) -> str:
        return f"{self.shirket_kassa} -> {self.holding_kassa} {self.transfer_meblegi} azn"


class HoldingdenShirketlereTransfer(models.Model):
    transfer_eden = models.ForeignKey(USER, on_delete=models.CASCADE, null=True,
                                      related_name="user_holding_shirket_transfer")
    holding_kassa = models.ForeignKey("cashbox.HoldingKassa", on_delete=models.CASCADE, null=True,
                                      related_name="holdingden_shirkete_transfer")
    shirket_kassa = models.ManyToManyField("cashbox.ShirketKassa", related_name="holdingden_shirkete_transfer")
    transfer_meblegi = models.FloatField(default=0)
    transfer_tarixi = models.DateField(auto_now=True)
    transfer_qeydi = models.TextField(null=True, blank=True)
    qalan_mebleg = models.FloatField(default=0, blank=True)
    evvelki_balans = models.FloatField(default=0, blank=True)
    sonraki_balans = models.FloatField(default=0, blank=True)

    class Meta:
        ordering = ("-pk",)

    def __str__(self) -> str:
        return f"{self.holding_kassa} -> {self.shirket_kassa} {self.transfer_meblegi} azn"

