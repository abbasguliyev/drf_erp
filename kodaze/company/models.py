from django.db import models
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model

USER = get_user_model()

# Create your models here.
class Holding(models.Model):
    holding_adi = models.CharField(max_length=200, unique=True)

    class Meta:
        ordering = ("pk",)

    def __str__(self) -> str:
        return self.holding_adi


class Shirket(models.Model):
    shirket_adi = models.CharField(max_length=200, unique=True)
    holding = models.ForeignKey(Holding, on_delete=models.CASCADE, related_name="holding_shirket")
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ("pk",)

    def __str__(self) -> str:
        return self.shirket_adi


class Ofis(models.Model):
    ofis_adi = models.CharField(max_length=100)
    shirket = models.ForeignKey(Shirket, on_delete=models.CASCADE, related_name="shirket_ofis")
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ("pk",)

    def __str__(self) -> str:
        return f"{self.ofis_adi} - {self.shirket}"


class Shobe(models.Model):
    shobe_adi = models.CharField(max_length=200)
    ofis = models.ForeignKey(Ofis, on_delete=models.CASCADE, null=True, related_name="shobe")
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ("pk",)

    def __str__(self) -> str:
        return f"{self.shobe_adi} - {self.ofis}"


class Vezifeler(models.Model):
    vezife_adi = models.CharField(max_length=50)
    shobe = models.ForeignKey(Shobe, on_delete=models.CASCADE, null=True, blank=True, related_name="shobe_vezife")
    shirket = models.ForeignKey(Shirket, on_delete=models.CASCADE, related_name="shirket_vezifeleri")
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs) -> None:
        self.vezife_adi = self.vezife_adi.upper()
        return super(Vezifeler, self).save(*args, **kwargs)

    class Meta:
        ordering = ("pk",)

    def __str__(self):
        return f"{self.vezife_adi}-{self.shirket}"


class Komanda(models.Model):
    komanda_adi = models.CharField(max_length=50, unique=True)
    is_active = models.BooleanField(
        default=True,
    )

    class Meta:
        ordering = ("pk",)

    def __str__(self):
        return self.komanda_adi


class VezifePermission(models.Model):
    vezife = models.ForeignKey(Vezifeler, on_delete=models.CASCADE, related_name="vezife_permission")
    permission_group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="vezife_permission")

    def __str__(self) -> str:
        return f"{self.vezife}-{self.permission_group}"
