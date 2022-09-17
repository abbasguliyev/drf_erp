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

    class Meta:
        ordering = ("-pk",)
        default_permissions = []
        permissions = (
            ("view_iscigelibgetmevaxtlari", "Mövcud işçi gəlib-getmə vaxtlarına baxa bilər"),
            ("add_iscigelibgetmevaxtlari", "İşçi gəlib-getmə vaxtı əlavə edə bilər"),
            ("change_iscigelibgetmevaxtlari", "İşçi gəlib-getmə vaxtının məlumatlarını yeniləyə bilər"),
            ("delete_iscigelibgetmevaxtlari", "İşçi gəlib-getmə vaxtını silə bilər")
        )

    # def __str__(self) -> str:
    #     return f"{self.isci} - {self.gelme_vaxti} - {self.getme_vaxti}"


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
        default_permissions = []
        permissions = (
            ("view_iscigunler", "Mövcud işçilərin tətil günlərinə baxa bilər"),
            ("add_iscigunler", "İşçilərə tətil günü əlavə edə bilər"),
            ("change_iscigunler", "İşçilərin tətil günü məlumatlarını yeniləyə bilər"),
            ("delete_iscigunler", "İşçilərin tətil gününü silə bilər")
        )

    # def __str__(self) -> str:
    #     return f"{self.isci} - {self.is_gunleri_count} - {self.tarix}"

class HoldingGunler(models.Model):
    holding = models.ForeignKey('company.Holding', on_delete=models.CASCADE, related_name="is_gunleri")
    is_gunleri_count = models.PositiveBigIntegerField(default=0)
    qeyri_is_gunu_count = models.PositiveBigIntegerField(default=0)
    tetil_gunleri = models.CharField(max_length=500, null=True, blank=True)
    tarix = models.DateField(default=datetime.now, blank=True)
    
    class Meta:
        ordering = ("pk",)
        default_permissions = []
        permissions = (
            ("view_holdinggunler", "Mövcud holdinq tətil günlərinə baxa bilər"),
            ("add_holdinggunler", "Holdinqə tətil günü əlavə edə bilər"),
            ("change_holdinggunler", "Holdinqin tətil günü məlumatlarını yeniləyə bilər"),
            ("delete_holdinggunler", "Holdinqin tətil gününü silə bilər")
        )

    # def __str__(self) -> str:
    #     return f"{self.holding} - {self.is_gunleri_count} - {self.tarix}"


class ShirketGunler(models.Model):
    shirket = models.ForeignKey('company.Shirket', on_delete=models.CASCADE, related_name="is_gunleri")
    is_gunleri_count = models.PositiveBigIntegerField(default=0)
    qeyri_is_gunu_count = models.PositiveBigIntegerField(default=0)
    tetil_gunleri = models.CharField(max_length=500, null=True, blank=True)
    tarix = models.DateField(default=datetime.now, blank=True)

    class Meta:
        ordering = ("pk",)
        default_permissions = []
        permissions = (
            ("view_shirketgunler", "Mövcud şirkət tətil günlərinə baxa bilər"),
            ("add_shirketgunler", "Şirkət tətil günü əlavə edə bilər"),
            ("change_shirketgunler", "Şirkətin tətil günü məlumatlarını yeniləyə bilər"),
            ("delete_shirketgunler", "Şirkətin tətil gününü silə bilər")
        )
  
    # def __str__(self) -> str:
    #     return f"{self.shirket} - {self.is_gunleri_count} - {self.tarix}"

class OfisGunler(models.Model):
    ofis = models.ForeignKey('company.Ofis', on_delete=models.CASCADE, related_name="is_gunleri")
    is_gunleri_count = models.PositiveBigIntegerField(default=0)
    qeyri_is_gunu_count = models.PositiveBigIntegerField(default=0)
    tetil_gunleri = models.CharField(max_length=500, null=True, blank=True)
    tarix = models.DateField(default=datetime.now, blank=True)

    class Meta:
        ordering = ("pk",)
        default_permissions = []
        permissions = (
            ("view_ofisgunler", "Mövcud ofis tətil günlərinə baxa bilər"),
            ("add_ofisgunler", "Ofis tətil günü əlavə edə bilər"),
            ("change_ofisgunler", "Ofisin tətil günü məlumatlarını yeniləyə bilər"),
            ("delete_ofisgunler", "Ofisin tətil gününü silə bilər")
        )

    # def __str__(self) -> str:
    #     return f"{self.ofis} - {self.is_gunleri_count} - {self.tarix}"

class KomandaGunler(models.Model):
    komanda = models.ForeignKey('company.Komanda', on_delete=models.CASCADE, related_name="is_gunleri")
    is_gunleri_count = models.PositiveBigIntegerField(default=0)
    qeyri_is_gunu_count = models.PositiveBigIntegerField(default=0)
    tetil_gunleri = models.CharField(max_length=500, null=True, blank=True)
    tarix = models.DateField(default=datetime.now, blank=True)

    class Meta:
        ordering = ("pk",)
        default_permissions = []
        permissions = (
            ("view_komandagunler", "Mövcud komanda tətil günlərinə baxa bilər"),
            ("add_komandagunler", "Komanda tətil günü əlavə edə bilər"),
            ("change_komandagunler", "Komandanın tətil günü məlumatlarını yeniləyə bilər"),
            ("delete_komandagunler", "Komandanın tətil gününü silə bilər")
        )

    # def __str__(self) -> str:
    #     return f"{self.komanda} - {self.is_gunleri_count} - {self.tarix}"

class VezifeGunler(models.Model):
    vezife = models.ForeignKey('company.Vezifeler', on_delete=models.CASCADE, related_name="is_gunleri")
    is_gunleri_count = models.PositiveBigIntegerField(default=0)
    qeyri_is_gunu_count = models.PositiveBigIntegerField(default=0)
    tetil_gunleri = models.CharField(max_length=500, null=True, blank=True)
    tarix = models.DateField(default=datetime.now, blank=True)

    class Meta:
        ordering = ("pk",)
        default_permissions = []
        permissions = (
            ("view_vezifegunler", "Mövcud vəzifə tətil günlərinə baxa bilər"),
            ("add_vezifegunler", "Vəzifə tətil günü əlavə edə bilər"),
            ("change_vezifegunler", "Vəzifənin tətil günü məlumatlarını yeniləyə bilər"),
            ("delete_vezifegunler", "Vəzifənin tətil gününü silə bilər")
        )

    # def __str__(self) -> str:
    #     return f"{self.vezife} - {self.is_gunleri_count} - {self.tarix}"

class ShobeGunler(models.Model):
    shobe = models.ForeignKey('company.Shobe', on_delete=models.CASCADE, related_name="is_gunleri")
    is_gunleri_count = models.PositiveBigIntegerField(default=0)
    qeyri_is_gunu_count = models.PositiveBigIntegerField(default=0)
    tetil_gunleri = models.CharField(max_length=500, null=True, blank=True)
    tarix = models.DateField(default=datetime.now, blank=True)

    class Meta:
        ordering = ("pk",)
        default_permissions = []
        permissions = (
            ("view_shobegunler", "Mövcud şöbə tətil günlərinə baxa bilər"),
            ("add_shobegunler", "Şöbə tətil günü əlavə edə bilər"),
            ("change_shobegunler", "Şöbənin tətil günü məlumatlarını yeniləyə bilər"),
            ("delete_shobegunler", "Şöbənin tətil gününü silə bilər")
        )

    # def __str__(self) -> str:
    #     return f"{self.shobe} - {self.is_gunleri_count} - {self.tarix}"


# ----------------------------------------------------------------------------------

class HoldingIstisnaIsci(IstisnaIsci):
    gunler = models.ForeignKey(HoldingGunler, on_delete=models.CASCADE, related_name="istisna_isci")

    class Meta:
        ordering = ("pk",)
        default_permissions = []
        permissions = (
            ("view_holdingistisnaisci", "Mövcud holdinq istisna işçilərə baxa bilər"),
            ("add_holdingistisnaisci", "Holdinq istisna işçi əlavə edə bilər"),
            ("change_holdingistisnaisci", "Holdinq istisna işçi məlumatlarını yeniləyə bilər"),
            ("delete_holdingistisnaisci", "Holdinq istisna işçiməlumatalrını silə bilər")
        )

    # def __str__(self) -> str:
    #     return f"{self.gunler} - {self.istisna_isciler} - {self.tetil_gunleri}"

class ShirketIstisnaIsci(IstisnaIsci):
    gunler = models.ForeignKey(ShirketGunler, on_delete=models.CASCADE, related_name="istisna_isci")

    class Meta:
        ordering = ("pk",)
        default_permissions = []
        permissions = (
            ("view_shirketistisnaisci", "Mövcud şirkət istisna işçilərə baxa bilər"),
            ("add_shirketistisnaisci", "Şirkət istisna işçi əlavə edə bilər"),
            ("change_shirketistisnaisci", "Şirkət istisna işçi məlumatlarını yeniləyə bilər"),
            ("delete_shirketistisnaisci", "Şirkət istisna işçiməlumatalrını silə bilər")
        )

    # def __str__(self) -> str:
    #     return f"{self.gunler} - {self.istisna_isciler} - {self.tetil_gunleri}"

class OfisIstisnaIsci(IstisnaIsci):
    gunler = models.ForeignKey(OfisGunler, on_delete=models.CASCADE, related_name="istisna_isci")

    class Meta:
        ordering = ("pk",)
        default_permissions = []
        permissions = (
            ("view_ofisistisnaisci", "Mövcud ofis istisna işçilərə baxa bilər"),
            ("add_ofisistisnaisci", "Ofis istisna işçi əlavə edə bilər"),
            ("change_ofisistisnaisci", "Ofis istisna işçi məlumatlarını yeniləyə bilər"),
            ("delete_ofisistisnaisci", "Ofis istisna işçiməlumatalrını silə bilər")
        )

    # def __str__(self) -> str:
    #     return f"{self.gunler} - {self.istisna_isciler} - {self.tetil_gunleri}"

class ShobeIstisnaIsci(IstisnaIsci):
    gunler = models.ForeignKey(ShobeGunler, on_delete=models.CASCADE, related_name="istisna_isci")

    class Meta:
        ordering = ("pk",)
        default_permissions = []
        permissions = (
            ("view_shobeistisnaisci", "Mövcud şöbə istisna işçilərə baxa bilər"),
            ("add_shobeistisnaisci", "Şöbə istisna işçi əlavə edə bilər"),
            ("change_shobeistisnaisci", "Şöbə istisna işçi məlumatlarını yeniləyə bilər"),
            ("delete_shobeistisnaisci", "Şöbə istisna işçiməlumatalrını silə bilər")
        )

    # def __str__(self) -> str:
    #     return f"{self.gunler} - {self.istisna_isciler} - {self.tetil_gunleri}"

class KomandaIstisnaIsci(IstisnaIsci):
    gunler = models.ForeignKey(KomandaGunler, on_delete=models.CASCADE, related_name="istisna_isci")

    class Meta:
        ordering = ("pk",)
        default_permissions = []
        permissions = (
            ("view_komandaistisnaisci", "Mövcud komanda istisna işçilərə baxa bilər"),
            ("add_komandaistisnaisci", "Komanda istisna işçi əlavə edə bilər"),
            ("change_komandaistisnaisci", "Komanda istisna işçi məlumatlarını yeniləyə bilər"),
            ("delete_komandaistisnaisci", "Komanda istisna işçiməlumatalrını silə bilər")
        )

    # def __str__(self) -> str:
    #     return f"{self.gunler} - {self.istisna_isciler} - {self.tetil_gunleri}"

class VezifeIstisnaIsci(IstisnaIsci):
    gunler = models.ForeignKey(VezifeGunler, on_delete=models.CASCADE, related_name="istisna_isci")

    class Meta:
        ordering = ("pk",)
        default_permissions = []
        permissions = (
            ("view_vezifeistisnaisci", "Mövcud vəzifə istisna işçilərə baxa bilər"),
            ("add_vezifeistisnaisci", "Vəzifə istisna işçi əlavə edə bilər"),
            ("change_vezifeistisnaisci", "Vəzifə istisna işçi məlumatlarını yeniləyə bilər"),
            ("delete_vezifeistisnaisci", "Vəzifə istisna işçiməlumatalrını silə bilər")
        )

    # def __str__(self) -> str:
    #     return f"{self.gunler} - {self.istisna_isciler} - {self.tetil_gunleri}"