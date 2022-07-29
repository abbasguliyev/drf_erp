from django.db import models
import pandas as pd
from datetime import datetime
from django.contrib.auth import get_user_model

USER = get_user_model()
# Create your models here.
class IstisnaIsci(models.Model):
    istisna_isciler = models.ManyToManyField(USER, blank=True)
    tetil_gunleri = models.CharField(max_length=500, null=True, blank=True)

    class Meta:
        abstract = True

class IsciGelibGetmeVaxtlari(models.Model):
    isci = models.ManyToManyField(USER, related_name="isci_gelib_getme_vaxtlari")
    gelme_vaxti = models.TimeField()
    getme_vaxti = models.TimeField()

    def __str__(self) -> str:
        return f"{self.isci} - {self.gelme_vaxti} - {self.getme_vaxti}"


class IsciGunler(models.Model):
    isci = models.ForeignKey(USER, on_delete=models.CASCADE, related_name="is_gunleri")
    is_gunleri_count = models.PositiveBigIntegerField(default=0)
    qeyri_is_gunu_count = models.PositiveBigIntegerField(default=0)
    tetil_gunleri = models.CharField(max_length=500, null=True, blank=True)
    icaze_gunleri_odenisli = models.CharField(max_length=500, null=True, blank=True)
    icaze_gunleri_odenissiz = models.CharField(max_length=500, null=True, blank=True)
    tarix = models.DateField(default=datetime.now, blank=True)
    is_odenisli = models.BooleanField(default=False)
    odenis_meblegi = models.FloatField(default=0, blank=True)

    class Meta:
        ordering = ("pk",)

    def __str__(self) -> str:
        return f"{self.isci} - {self.is_gunleri_count} - {self.tarix}"

class HoldingGunler(models.Model):
    holding = models.ForeignKey('company.Holding', on_delete=models.CASCADE, related_name="is_gunleri")
    is_gunleri_count = models.PositiveBigIntegerField(default=0)
    qeyri_is_gunu_count = models.PositiveBigIntegerField(default=0)
    tetil_gunleri = models.CharField(max_length=500, null=True, blank=True)
    tarix = models.DateField(default=datetime.now, blank=True)
    
    class Meta:
        ordering = ("pk",)

    def __str__(self) -> str:
        return f"{self.holding} - {self.is_gunleri_count} - {self.tarix}"


class ShirketGunler(models.Model):
    shirket = models.ForeignKey('company.Shirket', on_delete=models.CASCADE, related_name="is_gunleri")
    is_gunleri_count = models.PositiveBigIntegerField(default=0)
    qeyri_is_gunu_count = models.PositiveBigIntegerField(default=0)
    tetil_gunleri = models.CharField(max_length=500, null=True, blank=True)
    tarix = models.DateField(default=datetime.now, blank=True)

    class Meta:
        ordering = ("pk",)
  
    def __str__(self) -> str:
        return f"{self.shirket} - {self.is_gunleri_count} - {self.tarix}"

class OfisGunler(models.Model):
    ofis = models.ForeignKey('company.Ofis', on_delete=models.CASCADE, related_name="is_gunleri")
    is_gunleri_count = models.PositiveBigIntegerField(default=0)
    qeyri_is_gunu_count = models.PositiveBigIntegerField(default=0)
    tetil_gunleri = models.CharField(max_length=500, null=True, blank=True)
    tarix = models.DateField(default=datetime.now, blank=True)

    class Meta:
        ordering = ("pk",)

    def __str__(self) -> str:
        return f"{self.ofis} - {self.is_gunleri_count} - {self.tarix}"

class KomandaGunler(models.Model):
    komanda = models.ForeignKey('company.Komanda', on_delete=models.CASCADE, related_name="is_gunleri")
    is_gunleri_count = models.PositiveBigIntegerField(default=0)
    qeyri_is_gunu_count = models.PositiveBigIntegerField(default=0)
    tetil_gunleri = models.CharField(max_length=500, null=True, blank=True)
    tarix = models.DateField(default=datetime.now, blank=True)

    class Meta:
        ordering = ("pk",)

    def __str__(self) -> str:
        return f"{self.komanda} - {self.is_gunleri_count} - {self.tarix}"

class VezifeGunler(models.Model):
    vezife = models.ForeignKey('company.Vezifeler', on_delete=models.CASCADE, related_name="is_gunleri")
    is_gunleri_count = models.PositiveBigIntegerField(default=0)
    qeyri_is_gunu_count = models.PositiveBigIntegerField(default=0)
    tetil_gunleri = models.CharField(max_length=500, null=True, blank=True)
    tarix = models.DateField(default=datetime.now, blank=True)

    class Meta:
        ordering = ("pk",)

    def __str__(self) -> str:
        return f"{self.vezife} - {self.is_gunleri_count} - {self.tarix}"

class ShobeGunler(models.Model):
    shobe = models.ForeignKey('company.Shobe', on_delete=models.CASCADE, related_name="is_gunleri")
    is_gunleri_count = models.PositiveBigIntegerField(default=0)
    qeyri_is_gunu_count = models.PositiveBigIntegerField(default=0)
    tetil_gunleri = models.CharField(max_length=500, null=True, blank=True)
    tarix = models.DateField(default=datetime.now, blank=True)

    class Meta:
        ordering = ("pk",)

    def __str__(self) -> str:
        return f"{self.shobe} - {self.is_gunleri_count} - {self.tarix}"


# ----------------------------------------------------------------------------------

class HoldingIstisnaIsci(IstisnaIsci):
    gunler = models.ForeignKey(HoldingGunler, on_delete=models.CASCADE, related_name="istisna_isci")

    class Meta:
        ordering = ("pk",)

    def __str__(self) -> str:
        return f"{self.gunler} - {self.istisna_isciler} - {self.tetil_gunleri}"

class ShirketIstisnaIsci(IstisnaIsci):
    gunler = models.ForeignKey(ShirketGunler, on_delete=models.CASCADE, related_name="istisna_isci")

    class Meta:
        ordering = ("pk",)

    def __str__(self) -> str:
        return f"{self.gunler} - {self.istisna_isciler} - {self.tetil_gunleri}"

class OfisIstisnaIsci(IstisnaIsci):
    gunler = models.ForeignKey(OfisGunler, on_delete=models.CASCADE, related_name="istisna_isci")

    class Meta:
        ordering = ("pk",)

    def __str__(self) -> str:
        return f"{self.gunler} - {self.istisna_isciler} - {self.tetil_gunleri}"

class ShobeIstisnaIsci(IstisnaIsci):
    gunler = models.ForeignKey(ShobeGunler, on_delete=models.CASCADE, related_name="istisna_isci")

    class Meta:
        ordering = ("pk",)

    def __str__(self) -> str:
        return f"{self.gunler} - {self.istisna_isciler} - {self.tetil_gunleri}"

class KomandaIstisnaIsci(IstisnaIsci):
    gunler = models.ForeignKey(KomandaGunler, on_delete=models.CASCADE, related_name="istisna_isci")

    class Meta:
        ordering = ("pk",)

    def __str__(self) -> str:
        return f"{self.gunler} - {self.istisna_isciler} - {self.tetil_gunleri}"

class VezifeIstisnaIsci(IstisnaIsci):
    gunler = models.ForeignKey(VezifeGunler, on_delete=models.CASCADE, related_name="istisna_isci")

    class Meta:
        ordering = ("pk",)

    def __str__(self) -> str:
        return f"{self.gunler} - {self.istisna_isciler} - {self.tetil_gunleri}"