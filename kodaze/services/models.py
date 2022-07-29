import django
from django.db import models

# Create your models here.

class Servis(models.Model):
    kredit = models.BooleanField(default=False, blank=True)
    kredit_muddeti = models.IntegerField(default=0, blank=True)
    endirim = models.FloatField(default=0, blank=True)
    muqavile = models.ForeignKey("contract.Muqavile", related_name="servis_muqavile", null=True, on_delete=models.CASCADE)
    mehsullar = models.ManyToManyField("contract.Muqavile", related_name="servis_mehsul")
    servis_tarix = models.DateField(default=django.utils.timezone.now, blank=True)
    yerine_yetirildi = models.BooleanField(default=False)
    servis_qiymeti = models.FloatField(default=0, blank=True)
    ilkin_odenis = models.FloatField(default=0, blank=True)
    odenilecek_umumi_mebleg = models.FloatField(default=0, blank=True)
    operator_tesdiq = models.BooleanField(default=False)
    qeyd = models.TextField(default = "", blank=True)
    is_auto = models.BooleanField(default=False)
    create_date = models.DateField(default=django.utils.timezone.now, editable=False)

    class Meta:
        ordering = ("-pk",)

    def __str__(self) -> str:
        return f"{self.pk}.servis-{self.muqavile}"

class ServisOdeme(models.Model):
    servis = models.ForeignKey(Servis, related_name="servis_odeme", null=True, on_delete=models.CASCADE)
    odenilecek_umumi_mebleg = models.FloatField(default=0, blank=True)
    odenilecek_mebleg = models.FloatField(default=0, blank=True)
    odendi = models.BooleanField(default=False)
    odeme_tarix = models.DateField(default=django.utils.timezone.now, blank=True)

    class Meta:
        ordering = ("-pk",)

    def __str__(self) -> str:
        return f"servis-{self.servis}-{self.odenilecek_mebleg}-{self.odendi}"
