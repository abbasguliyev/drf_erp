from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator
from core.image_validator import file_size

USER = get_user_model()

# Create your models here.
class HoldingKassaMedaxil(models.Model):
    medaxil_eden = models.ForeignKey(USER, on_delete=models.SET_NULL, null=True,
                                     related_name="user_holding_medaxil")
    holding_kassa = models.ForeignKey("cashbox.HoldingKassa", on_delete=models.CASCADE, null=True,
                                      related_name="holding_kassa_medaxil")
    mebleg = models.FloatField(default=0)
    qeyd = models.TextField(null=True, blank=True)
    medaxil_tarixi = models.DateField(default=None)
    evvelki_balans = models.FloatField(default=0, blank=True)
    sonraki_balans = models.FloatField(default=0, blank=True)

    class Meta:
        ordering = ("-pk",)

    def __str__(self) -> str:
        return f"{self.holding_kassa} kassasına {self.mebleg} azn mədaxil edildi"


class HoldingKassaMexaric(models.Model):
    mexaric_eden = models.ForeignKey(USER, on_delete=models.SET_NULL, null=True,
                                     related_name="user_holding_mexaric")
    holding_kassa = models.ForeignKey("cashbox.HoldingKassa", on_delete=models.CASCADE, null=True,
                                      related_name="holding_kassa_mexaric")
    mebleg = models.FloatField(default=0)
    qebzin_resmi = models.ImageField(upload_to="media/%Y/%m/%d/", null=True, blank=True, validators=[file_size, FileExtensionValidator(['png', 'jpeg', 'jpg'])])
    qeyd = models.TextField(null=True, blank=True)
    mexaric_tarixi = models.DateField(default=None)
    evvelki_balans = models.FloatField(default=0, blank=True)
    sonraki_balans = models.FloatField(default=0, blank=True)

    class Meta:
        ordering = ("-pk",)

    def __str__(self) -> str:
        return f"{self.holding_kassa} kassasından {self.mebleg} azn məxaric edildi"


# -----------------------------------------------------

class ShirketKassaMedaxil(models.Model):
    medaxil_eden = models.ForeignKey(USER, on_delete=models.SET_NULL, null=True,
                                     related_name="user_shirket_medaxil")
    shirket_kassa = models.ForeignKey("cashbox.ShirketKassa", on_delete=models.CASCADE, null=True,
                                      related_name="shirket_kassa_medaxil")
    mebleg = models.FloatField(default=0)
    qeyd = models.TextField(null=True, blank=True)
    medaxil_tarixi = models.DateField(default=None)
    evvelki_balans = models.FloatField(default=0, blank=True)
    sonraki_balans = models.FloatField(default=0, blank=True)

    class Meta:
        ordering = ("-pk",)

    def __str__(self) -> str:
        return f"{self.shirket_kassa} kassasına {self.mebleg} azn mədaxil edildi"


class ShirketKassaMexaric(models.Model):
    mexaric_eden = models.ForeignKey(USER, on_delete=models.SET_NULL, null=True,
                                     related_name="user_shirket_mexaric")
    shirket_kassa = models.ForeignKey("cashbox.ShirketKassa", on_delete=models.CASCADE, null=True,
                                      related_name="shirket_kassa_mexaric")
    mebleg = models.FloatField(default=0)
    qebzin_resmi = models.ImageField(upload_to="media/%Y/%m/%d/", null=True, blank=True, validators=[file_size, FileExtensionValidator(['png', 'jpeg', 'jpg'])])
    qeyd = models.TextField(null=True, blank=True)
    mexaric_tarixi = models.DateField(default=None)
    evvelki_balans = models.FloatField(default=0, blank=True)
    sonraki_balans = models.FloatField(default=0, blank=True)

    class Meta:
        ordering = ("-pk",)

    def __str__(self) -> str:
        return f"{self.shirket_kassa} kassasından {self.mebleg} azn məxaric edildi"


# -----------------------------------------------------

class OfisKassaMedaxil(models.Model):
    medaxil_eden = models.ForeignKey(USER, on_delete=models.SET_NULL, null=True,
                                     related_name="user_ofis_medaxil")
    ofis_kassa = models.ForeignKey("cashbox.OfisKassa", on_delete=models.CASCADE, null=True, related_name="ofis_kassa_medaxil")
    mebleg = models.FloatField(default=0)
    qeyd = models.TextField(null=True, blank=True)
    medaxil_tarixi = models.DateField(default=None)
    evvelki_balans = models.FloatField(default=0, blank=True)
    sonraki_balans = models.FloatField(default=0, blank=True)

    class Meta:
        ordering = ("-pk",)

    def __str__(self) -> str:
        return f"{self.ofis_kassa} kassasına {self.mebleg} azn mədaxil edildi"


class OfisKassaMexaric(models.Model):
    mexaric_eden = models.ForeignKey(USER, on_delete=models.SET_NULL, null=True,
                                     related_name="user_ofis_mexaric")
    ofis_kassa = models.ForeignKey("cashbox.OfisKassa", on_delete=models.CASCADE, null=True, related_name="ofis_kassa_mexaric")
    mebleg = models.FloatField(default=0)
    qebzin_resmi = models.ImageField(upload_to="media/%Y/%m/%d/", null=True, blank=True, validators=[file_size, FileExtensionValidator(['png', 'jpeg', 'jpg'])])
    qeyd = models.TextField(null=True, blank=True)
    mexaric_tarixi = models.DateField(default=None)
    evvelki_balans = models.FloatField(default=0, blank=True)
    sonraki_balans = models.FloatField(default=0, blank=True)

    class Meta:
        ordering = ("-pk",)

    def __str__(self) -> str:
        return f"{self.ofis_kassa} kassasından {self.mebleg} azn məxaric edildi"
