from django.db import models
import django
from core.image_validator import file_size
from django.core.validators import FileExtensionValidator
from django.contrib.auth import get_user_model

from . import (
    ODENIS_USLUBU_CHOICES,
    NAGD,
    KREDIT,
    YENI_QRAFIK_CHOICES,
    DEYISMIS_MEHSUL_STATUS_CHOICES,
    MUQAVILE_STATUS_CHOICES,
    DAVAM_EDEN,
    ILKIN_ODENIS_STATUS_CHOICES,
    YOXDUR,
    QALIQ_ILKIN_ODENIS_STATUS_CHOICES,
    ODEME_STATUS_CHOICES,
    ODENMEYEN,
    SERTLI_ODEME_STATUSU,
    BORCU_BAGLA_STATUS_CHOICES,
    GECIKDIRME_STATUS_CHOICES,
    SIFIR_STATUS_CHOICES,
    NATAMAM_STATUS_CHOICES,
    ARTIQ_ODEME_STATUS_CHOICES,
)

USER = get_user_model()


# Create your models here.
class Muqavile(models.Model):
    group_leader = models.ForeignKey('account.User', on_delete=models.CASCADE, related_name="group_leader", null=True,
                                     blank=True)
    menecer1 = models.ForeignKey('account.User', on_delete=models.CASCADE, related_name="menecer1", null=True,
                                 blank=True)
    menecer2 = models.ForeignKey('account.User', on_delete=models.CASCADE, related_name="menecer2", null=True,
                                 blank=True)
    musteri = models.ForeignKey('account.Musteri', on_delete=models.CASCADE, related_name="musteri_muqavile", null=True,
                                blank=True)
    mehsul = models.ForeignKey("product.Mehsullar", on_delete=models.CASCADE, related_name="mehsul_muqavile", null=True,
                               blank=True)
    mehsul_sayi = models.PositiveIntegerField(default=1, blank=True)
    muqavile_umumi_mebleg = models.FloatField(default=0, blank=True)
    elektron_imza = models.ImageField(upload_to="media/muqavile/%Y/%m/%d/", null=True, blank=True,
                                      validators=[file_size, FileExtensionValidator(['png', 'jpeg', 'jpg'])])
    muqavile_tarixi = models.DateField(null=True, blank=True)
    muqavile_imzalanma_tarixi = models.DateField(auto_now_add=True)
    shirket = models.ForeignKey('company.Shirket', on_delete=models.CASCADE, related_name="muqavile", null=True,
                                blank=True)
    ofis = models.ForeignKey('company.Ofis', on_delete=models.CASCADE, related_name="muqavile", null=True, blank=True)
    qaliq_borc = models.FloatField(default=0, blank=True)
    is_sokuntu = models.BooleanField(default=False)

    odenis_uslubu = models.CharField(
        max_length=20,
        choices=ODENIS_USLUBU_CHOICES,
        default=NAGD
    )

    yeni_qrafik_mebleg = models.FloatField(default=0, blank=True)
    yeni_qrafik_status = models.CharField(
        max_length=50,
        choices=YENI_QRAFIK_CHOICES,
        default=None,
        null=True,
        blank=True
    )

    deyisilmis_mehsul_status = models.CharField(
        max_length=50,
        choices=DEYISMIS_MEHSUL_STATUS_CHOICES,
        default=None,
        null=True,
        blank=True
    )

    muqavile_status = models.CharField(
        max_length=20,
        choices=MUQAVILE_STATUS_CHOICES,
        default=DAVAM_EDEN
    )

    kredit_muddeti = models.IntegerField(default=0, blank=True)
    ilkin_odenis = models.FloatField(blank=True, default=0)
    ilkin_odenis_qaliq = models.FloatField(blank=True, default=0)
    ilkin_odenis_tarixi = models.DateField(blank=True, null=True)
    ilkin_odenis_qaliq_tarixi = models.DateField(blank=True, null=True)

    ilkin_odenis_status = models.CharField(
        max_length=20,
        choices=ILKIN_ODENIS_STATUS_CHOICES,
        default=YOXDUR
    )

    qaliq_ilkin_odenis_status = models.CharField(
        max_length=20,
        choices=QALIQ_ILKIN_ODENIS_STATUS_CHOICES,
        default=YOXDUR
    )
    pdf = models.FileField(upload_to="media/media/muqavile_doc/%Y/%m/%d/", blank=True, null=True,
                           validators=[file_size, FileExtensionValidator(['pdf'])])
    pdf_elave = models.FileField(upload_to="media/media/muqavile_doc/%Y/%m/%d/", blank=True, null=True,
                                 validators=[file_size, FileExtensionValidator(['pdf'])])

    dusme_tarixi = models.DateField(null=True, blank=True)
    borc_baglanma_tarixi = models.DateField(null=True, blank=True)

    kompensasiya_medaxil = models.FloatField(default=0, null=True, blank=True)
    kompensasiya_mexaric = models.FloatField(default=0, null=True, blank=True)

    borc_baglandi = models.BooleanField(default=False, blank=True)
    qeyd = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ("-pk",)
        default_permissions = []
        permissions = (
            ("view_muqavile", "Mövcud müqavilələrə baxa bilər"),
            ("add_muqavile", "Müqavilə əlavə edə bilər"),
            ("change_muqavile", "Müqavilə məlumatlarını yeniləyə bilər"),
            ("delete_muqavile", "Müqavilə silə bilər")
        )


class MuqavileHediyye(models.Model):
    mehsul = models.ManyToManyField("product.Mehsullar", related_name="mehsul_hediyye")
    muqavile = models.ForeignKey(Muqavile, on_delete=models.CASCADE, related_name="muqavile_hediyye")
    ofis = models.ForeignKey('company.Ofis', on_delete=models.CASCADE, null=True, related_name="ofis_muqavile_hediyye")
    say = models.PositiveBigIntegerField(default=1)
    hediyye_tarixi = models.DateField(auto_now_add=True, null=True)

    class Meta:
        ordering = ("pk",)
        default_permissions = []
        permissions = (
            ("view_muqavilehediyye", "Mövcud müqavilə hədiyyələrə baxa bilər"),
            ("add_muqavilehediyye", "Müqavilə hədiyyə əlavə edə bilər"),
            ("change_muqavilehediyye", "Müqavilə hədiyyə məlumatlarını yeniləyə bilər"),
            ("delete_muqavilehediyye", "Müqavilə hədiyyə silə bilər")
        )


class OdemeTarix(models.Model):
    ay_no = models.PositiveIntegerField(default=1)
    muqavile = models.ForeignKey(Muqavile, blank=True, null=True, related_name='odeme_tarixi',
                                 on_delete=models.CASCADE)
    tarix = models.DateField(default=False, blank=True, null=True)
    qiymet = models.FloatField(default=0, blank=True)
    odenme_status = models.CharField(
        max_length=30,
        choices=ODEME_STATUS_CHOICES,
        default=ODENMEYEN
    )

    sertli_odeme_status = models.CharField(
        max_length=50,
        choices=SERTLI_ODEME_STATUSU,
        default=None,
        null=True,
        blank=True
    )

    borcu_bagla_status = models.CharField(
        max_length=30,
        choices=BORCU_BAGLA_STATUS_CHOICES,
        default=None,
        null=True,
        blank=True
    )

    gecikdirme_status = models.CharField(
        max_length=30,
        choices=GECIKDIRME_STATUS_CHOICES,
        default=None,
        null=True,
        blank=True
    )

    buraxilmis_ay_alt_status = models.CharField(
        max_length=20,
        choices=SIFIR_STATUS_CHOICES,
        default=None,
        null=True,
        blank=True
    )

    natamam_ay_alt_status = models.CharField(
        max_length=20,
        choices=NATAMAM_STATUS_CHOICES,
        default=None,
        null=True,
        blank=True
    )

    artiq_odeme_alt_status = models.CharField(
        max_length=20,
        choices=ARTIQ_ODEME_STATUS_CHOICES,
        default=None,
        null=True,
        blank=True
    )

    sonuncu_ay = models.BooleanField(default=False)
    qeyd = models.TextField(default="", blank=True)

    class Meta:
        ordering = ("pk",)
        default_permissions = []
        permissions = (
            ("view_odemetarix", "Mövcud ödəmələrə baxa bilər"),
            ("add_odemetarix", "Ödəmə əlavə edə bilər"),
            ("change_odemetarix", "Ödəmə məlumatlarını yeniləyə bilər"),
            ("delete_odemetarix", "Ödəmə silə bilər")
        )


class Deyisim(models.Model):
    kohne_muqavile = models.ForeignKey(Muqavile, related_name="deyisim", on_delete=models.CASCADE)
    odenis_uslubu = models.CharField(max_length=100, choices=ODENIS_USLUBU_CHOICES, default=KREDIT)
    kredit_muddeti = models.IntegerField(default=0, blank=True)
    mehsul = models.ForeignKey("product.Mehsullar", related_name="deyisim", on_delete=models.CASCADE)

    class Meta:
        ordering = ("-pk",)
        default_permissions = []
        permissions = (
            ("view_deyisim", "Mövcud dəyişimlərə baxa bilər"),
            ("add_deyisim", "Dəyişim əlavə edə bilər"),
            ("change_deyisim", "Dəyişim məlumatlarını yeniləyə bilər"),
            ("delete_deyisim", "Dəyişim silə bilər")
        )


class DemoSatis(models.Model):
    user = models.ForeignKey(USER, on_delete=models.CASCADE, related_name="demos")
    count = models.IntegerField(default=0)
    created_date = models.DateField(default=django.utils.timezone.now, blank=True)
    sale_count = models.IntegerField(default=0)

    class Meta:
        ordering = ("-pk",)
        default_permissions = []
        permissions = (
            ("view_demosatis", "Mövcud demo satışlara baxa bilər"),
            ("add_demosatis", "Demo satış əlavə edə bilər"),
            ("change_demosatis", "Demo satış məlumatlarını yeniləyə bilər"),
            ("delete_demosatis", "Demo satış silə bilər")
        )


class MuqavileKreditor(models.Model):
    kreditor = models.ForeignKey(USER, on_delete=models.CASCADE, related_name="muqavile_kreditor")
    muqavile = models.ForeignKey(Muqavile, on_delete=models.CASCADE, related_name="kreditor")

    class Meta:
        ordering = ("-pk",)
        default_permissions = []
        permissions = (
            ("view_muqavilekreditor", "Mövcud kreditorlara baxa bilər"),
            ("add_muqavilekreditor", "Müqavilə Kreditor əlavə edə bilər"),
            ("change_muqavilekreditor", "Müqavilə Kreditor məlumatlarını yeniləyə bilər"),
            ("delete_muqavilekreditor", "Müqavilə Kreditor silə bilər")
        )
