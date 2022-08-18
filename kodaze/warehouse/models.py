import django
from django.db import models
from django.core.validators import FileExtensionValidator
from account.models import User
from core.image_validator import file_size
from django.contrib.auth import get_user_model

User = get_user_model()


class Anbar(models.Model):
    ad = models.CharField(max_length=100)
    ofis = models.ForeignKey(
        'company.Ofis', on_delete=models.CASCADE, null=True, related_name="ofis_anbar")
    shirket = models.ForeignKey(
        'company.Shirket', on_delete=models.CASCADE, null=True, related_name="shirket_anbar")
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ("pk",)
        default_permissions = []
        permissions = (
            ("view_anbar", "Mövcud anbarlara baxa bilər"),
            ("add_anbar", "Anbar əlavə edə bilər"),
            ("change_anbar", "Anbar məlumatlarını yeniləyə bilər"),
            ("delete_anbar", "Anbar silə bilər")
        )

    def __str__(self) -> str:
        return f"{self.ad} - {self.ofis}"


class AnbarQeydler(models.Model):
    gonderen_user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, related_name="anbar_sorgu")
    mehsul_ve_sayi = models.CharField(max_length=250, null=True, blank=True)
    qeyd = models.TextField()
    anbar = models.ForeignKey(
        Anbar, on_delete=models.CASCADE, related_name="anbar_qeyd")
    yerine_yetirildi = models.BooleanField(default=False)
    gonderilme_tarixi = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ("-pk",)
        default_permissions = []
        permissions = (
            ("view_anbarqeydler", "Mövcud anbar sorğularına baxa bilər"),
            ("add_anbarqeydler", "Anbar sorğu əlavə edə bilər"),
            ("change_anbarqeydler", "Anbar sorğu məlumatlarını yeniləyə bilər"),
            ("delete_anbarqeydler", "Anbar sorğu silə bilər")
        )

    def __str__(self) -> str:
        return f"{self.anbar} - {self.qeyd[:30]}"


class Stok(models.Model):
    anbar = models.ForeignKey(Anbar, null=True, on_delete=models.CASCADE)
    mehsul = models.ForeignKey(
        "product.Mehsullar", null=True, on_delete=models.CASCADE)
    say = models.IntegerField(default=0)
    tarix = models.DateField(auto_now=True, blank=True)
    qeyd = models.TextField(default="", null=True, blank=True)

    class Meta:
        ordering = ("pk",)
        default_permissions = []
        permissions = (
            ("view_stok", "Mövcud stoklara baxa bilər"),
            ("add_stok", "Stok əlavə edə bilər"),
            ("change_stok", "Stok məlumatlarını yeniləyə bilər"),
            ("delete_stok", "Stok silə bilər")
        )

    def __str__(self) -> str:
        return f"stok -> {self.anbar} - {self.mehsul} - {self.say}"


class Emeliyyat(models.Model):
    # mehsulun_sayi = models.IntegerField(default=0)
    # gonderilen_mehsul = models.ManyToManyField(Mehsullar, related_name="gonderilen_mehsul")
    TRANSFER = 'transfer'
    STOK_YENILEME = 'stok yeniləmə'

    EMELIYYAT_NOVU_CHOICES = [
        (TRANSFER, "transfer"),
        (STOK_YENILEME, "stok yeniləmə"),
    ]

    gonderen = models.ForeignKey(
        Anbar, on_delete=models.CASCADE, null=True, related_name="gonderen")
    qebul_eden = models.ForeignKey(
        Anbar, on_delete=models.CASCADE, null=True, related_name="qebul_eden")

    mehsul_ve_sayi = models.CharField(max_length=500, null=True, blank=True)

    qeyd = models.TextField(default="", null=True, blank=True)
    emeliyyat_tarixi = models.DateField(
        auto_now_add=True, null=True, blank=True)

    emeliyyat_novu = models.CharField(
        max_length=50, choices=EMELIYYAT_NOVU_CHOICES, default=TRANSFER)

    say = models.IntegerField(default=0, blank=True, null=True)
    icraci = models.ForeignKey(
        User, related_name="emeliyyat", on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ("pk",)
        default_permissions = []
        permissions = (
            ("view_emeliyyat", "Mövcud əməliyyatlara baxa bilər"),
            ("add_emeliyyat", "Əməliyyat əlavə edə bilər"),
            ("change_emeliyyat", "Əməliyyat məlumatlarını yeniləyə bilər"),
            ("delete_emeliyyat", "Əməliyyat silə bilər")
        )

    def __str__(self) -> str:
        return f"Əməliyyat ==> {self.gonderen} - {self.qebul_eden} {self.emeliyyat_tarixi}"
