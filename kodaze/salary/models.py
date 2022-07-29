import django
from django.db import models
import datetime
from django.contrib.auth import get_user_model

USER = get_user_model()
class AbstractPrim(models.Model):
    KREDIT = 'KREDİT'
    NAGD = 'NƏĞD'
    ODENIS_USLUBU_CHOICES = [
        (KREDIT, "KREDİT"),
        (NAGD, "NƏĞD"),
    ]

    prim_status = models.ForeignKey('account.IsciStatus', on_delete=models.SET_NULL, null=True)
    mehsul = models.ForeignKey('product.Mehsullar', on_delete=models.CASCADE, null=True, blank=True)
    satis_meblegi = models.FloatField(default=0, null=True, blank=True)
    odenis_uslubu =  models.CharField(
        max_length=20,
        choices=ODENIS_USLUBU_CHOICES,
        default=NAGD
    )
    vezife = models.ForeignKey('company.Vezifeler', on_delete=models.SET_NULL, null=True)

    class Meta:
        abstract = True

class VanLeaderPrim(AbstractPrim):
    komandaya_gore_prim = models.FloatField(default=0, blank=True)
    fix_maas = models.FloatField(default=0, blank=True)

    def __str__(self) -> str:
        return f"{self.prim_status} - {self.komandaya_gore_prim} - {self.odenis_uslubu} - {self.vezife.vezife_adi}"

class VanLeaderPrimNew(AbstractPrim):
    odenis_uslubu = None
    negd = models.FloatField(default=0, blank=True)
    kredit_4_12 = models.FloatField(default=0, blank=True)
    kredit_13_18 = models.FloatField(default=0, blank=True)
    kredit_19_24 = models.FloatField(default=0, blank=True)

    def __str__(self) -> str:
        return f"{self.prim_status} - {self.vezife.vezife_adi}"

class DealerPrim(AbstractPrim):
    komandaya_gore_prim = models.FloatField(default=0, blank=True)
    fix_maas = models.FloatField(default=0, blank=True)

    def __str__(self) -> str:
        return f"{self.prim_status} - {self.komandaya_gore_prim} - {self.odenis_uslubu} - {self.vezife.vezife_adi}"

class DealerPrimNew(AbstractPrim):
    odenis_uslubu = None
    negd = models.FloatField(default=0, blank=True)
    kredit_4_12 = models.FloatField(default=0, blank=True)
    kredit_13_18 = models.FloatField(default=0, blank=True)
    kredit_19_24 = models.FloatField(default=0, blank=True)

    def __str__(self) -> str:
        return f"{self.prim_status} - {self.vezife.vezife_adi}"

class OfficeLeaderPrim(AbstractPrim):
    odenis_uslubu = None
    ofise_gore_prim = models.FloatField(default=0, blank=True)
    fix_maas = models.FloatField(default=0, blank=True)

    def __str__(self) -> str:
        return f"{self.prim_status} - {self.ofise_gore_prim} - {self.vezife.vezife_adi}"

class CanvasserPrim(AbstractPrim):
    odenis_uslubu = None
    satis0 = models.FloatField(default=0, blank=True)
    satis1_8 = models.FloatField(default=0, blank=True)
    satis9_14 = models.FloatField(default=0, blank=True)
    satis15p = models.FloatField(default=0, blank=True)
    satis20p = models.FloatField(default=0, blank=True)
    komandaya_gore_prim = models.FloatField(default=0, blank=True)
    ofise_gore_prim = models.FloatField(default=0, blank=True)
    fix_maas = models.FloatField(default=0, blank=True)

    def __str__(self) -> str:
        return f"{self.prim_status} - {self.ofise_gore_prim} - {self.vezife.vezife_adi}"

class KreditorPrim(models.Model):
    prim_faizi = models.PositiveBigIntegerField(default=0, blank=True)

    def __str__(self) -> str:
        return f"{self.prim_faizi}"

# -----------------------------------------------------------------------------------------------------------------------------

class Avans(models.Model):
    isci = models.ManyToManyField(USER, related_name="isci_avans")
    mebleg = models.FloatField(default=0, blank=True)
    yarim_ay_emek_haqqi = models.PositiveBigIntegerField(default=0, blank=True)
    qeyd = models.TextField(default="", blank=True)
    avans_tarixi = models.DateField(default=django.utils.timezone.now, blank=True)
    
    class Meta:
        ordering = ("pk",)

    def __str__(self) -> str:
        return f"{self.isci} {self.avans_tarixi}"

class MaasOde(models.Model):
    isci = models.ManyToManyField(USER, related_name="maas_ode")
    mebleg = models.FloatField(default=0, blank=True)
    qeyd = models.TextField(default="", blank=True)
    odeme_tarixi = models.DateField(default=django.utils.timezone.now, null=True, blank=True)
    
    class Meta:
        ordering = ("pk",)

    def __str__(self) -> str:
        return f"{self.isci} {self.odeme_tarixi}"

class Kesinti(models.Model):
    isci = models.ForeignKey(USER, on_delete=models.CASCADE, related_name="isci_kesinti")
    mebleg = models.FloatField(default=0, blank=True)
    qeyd = models.TextField(default="", blank=True)
    kesinti_tarixi = models.DateField(default=django.utils.timezone.now, blank=True)
    
    class Meta:
        ordering = ("pk",)

    def __str__(self) -> str:
        return f"{self.isci} {self.kesinti_tarixi}"

class Bonus(models.Model):
    isci = models.ForeignKey(USER, on_delete=models.CASCADE, related_name="isci_bonus")
    mebleg = models.FloatField(default=0, blank=True)
    qeyd = models.TextField(default="", blank=True)
    bonus_tarixi = models.DateField(default=django.utils.timezone.now, blank=True)
    
    class Meta:
        ordering = ("pk",)

    def __str__(self) -> str:
        return f"{self.isci} {self.mebleg} {self.bonus_tarixi}"
 
class MaasGoruntuleme(models.Model):
    isci = models.ForeignKey(USER, on_delete=models.CASCADE, related_name="isci_maas_goruntuleme")
    satis_sayi = models.PositiveBigIntegerField(default=0, blank=True)
    satis_meblegi = models.FloatField(default=0, blank=True)
    yekun_maas = models.FloatField(default=0, blank=True)
    tarix = models.DateField(null=True, blank=True)
    odendi = models.BooleanField(default=False)

    class Meta:
        ordering = ("pk",)

    def __str__(self) -> str:
        return f"{self.isci} {self.yekun_maas} {self.tarix}"