from django.db import models
import django
from django.contrib.auth import get_user_model

USER = get_user_model()
# Create your models here.
class OfisKassa(models.Model):
    ofis = models.ForeignKey("company.Ofis", on_delete=models.CASCADE, related_name="ofis_kassa")
    balans = models.FloatField(default=0)

    class Meta:
        ordering = ("pk",)
        default_permissions = []
        permissions = (
            ("view_ofiskassa", "Mövcud ofis kassalara baxa bilər"),
            ("add_ofiskassa", "Ofis kassa əlavə edə bilər"),
            ("change_ofiskassa", "Ofis kassa məlumatlarını yeniləyə bilər"),
            ("delete_ofiskassa", "Ofis kassa silə bilər")
        )

    def __str__(self) -> str:
        return f"{self.ofis} -> {self.balans}"


class ShirketKassa(models.Model):
    shirket = models.ForeignKey("company.Shirket", on_delete=models.CASCADE, related_name="shirket_kassa")
    balans = models.FloatField(default=0)

    class Meta:
        ordering = ("pk",)
        default_permissions = []
        permissions = (
            ("view_shirketkassa", "Mövcud şirkət kassalara baxa bilər"),
            ("add_shirketkassa", "Şirkət kassa əlavə edə bilər"),
            ("change_shirketkassa", "Şirkət kassa məlumatlarını yeniləyə bilər"),
            ("delete_shirketkassa", "Şirkət kassa silə bilər")
        )

    def __str__(self) -> str:
        return f"{self.shirket} -> {self.balans}"


class HoldingKassa(models.Model):
    holding = models.ForeignKey("company.Holding", on_delete=models.CASCADE, related_name="holding_kassa")
    balans = models.FloatField(default=0)

    class Meta:
        ordering = ("pk",)
        default_permissions = []
        permissions = (
            ("view_holdingkassa", "Mövcud holdinq kassalara baxa bilər"),
            ("add_holdingkassa", "Holdinq kassa əlavə edə bilər"),
            ("change_holdingkassa", "Holdinq kassa məlumatlarını yeniləyə bilər"),
            ("delete_holdingkassa", "Holdinq kassa silə bilər")
        )

    def __str__(self) -> str:
        return f"{self.holding} -> {self.balans}"

# -----------------------------------------------------

class PulAxini(models.Model):
    MEDAXİL = "MƏDAXİL"
    MEXARIC = "MƏXARİC"
    TRANSFER = "TRANSFER"
    
    EMELIYYAT_USLUBU_CHOICE = [
        (MEDAXİL, "MƏDAXİL"),
        (MEXARIC, "MƏXARİC"),
        (TRANSFER, "TRANSFER"),
    ]

    tarix = models.DateField(default=django.utils.timezone.now, blank=True)
    holding = models.ForeignKey('company.Holding', on_delete=models.CASCADE, null=True, blank=True, related_name="pul_axinlari")
    shirket = models.ForeignKey('company.Shirket', on_delete=models.CASCADE, null=True, blank=True, related_name="pul_axinlari")
    ofis = models.ForeignKey('company.Ofis', on_delete=models.CASCADE, null=True, blank=True)
    aciqlama = models.TextField(null=True, blank=True)
    ilkin_balans = models.FloatField(default=0)
    sonraki_balans = models.FloatField(default=0)

    holding_ilkin_balans = models.FloatField(default=0)
    holding_sonraki_balans = models.FloatField(default=0)
    
    shirket_ilkin_balans = models.FloatField(default=0)
    shirket_sonraki_balans = models.FloatField(default=0)
    
    ofis_ilkin_balans = models.FloatField(default=0)
    ofis_sonraki_balans = models.FloatField(default=0)
    
    emeliyyat_eden = models.ForeignKey(USER, related_name="pul_axinlari", on_delete=models.CASCADE, null=True, blank=True)
    emeliyyat_uslubu = models.CharField(max_length=100, choices=EMELIYYAT_USLUBU_CHOICE, default=None, null=True, blank=True)
    miqdar = models.FloatField(default=0)

    class Meta:
        ordering = ("-pk",)
        default_permissions = []
        permissions = (
            ("view_pulaxini", "Mövcud pul axınlarına baxa bilər"),
            ("add_pulaxini", "Pul axını əlavə edə bilər"),
            ("change_pulaxini", "Pul axını məlumatlarını yeniləyə bilər"),
            ("delete_pulaxini", "Pul axını məlumatlarını silə bilər")
        )