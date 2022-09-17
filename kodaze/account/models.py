from email.policy import default
from django.db import models
import django
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from django.core.validators import FileExtensionValidator

from .managers import CustomUserManager
from core.image_validator import file_size
from . import (
    CONTRACT_TYPE_CHOICES,
    SALARY_STYLE_CHOICES,
    MONTHLY,
    CUSTOMER_TYPE_CHOICES,
    STANDART,
)

class IsciStatus(models.Model):
    status_adi = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.status_adi

    class Meta:
        ordering = ("pk",)
        default_permissions = []
        permissions = (
            ("view_iscistatus", "Mövcud işçi statuslarına baxa bilər"),
            ("add_iscistatus", "İşçi statusu əlavə edə bilər"),
            ("change_iscistatus", "İşçi statusu məlumatlarını yeniləyə bilər"),
            ("delete_iscistatus", "İşçi statusunu silə bilər")
        )


class User(AbstractUser):
    first_name = None
    last_name = None

    asa = models.CharField(max_length=200)
    dogum_tarixi = models.DateField(null=True, blank=True)
    ishe_baslama_tarixi = models.DateField(
        default=django.utils.timezone.now, null=True, blank=True)
    ishden_cixma_tarixi = models.DateField(null=True, blank=True)
    tel1 = models.CharField(max_length=200)
    tel2 = models.CharField(max_length=200, null=True, blank=True)
    tag = models.ForeignKey(
        'company.Tag', on_delete=models.SET_NULL, null=True, blank=True)
    sv_image = models.ImageField(upload_to="media/account/%Y/%m/%d/", null=True, blank=True,
                                 validators=[file_size, FileExtensionValidator(['png', 'jpeg', 'jpg'])])
    sv_image2 = models.ImageField(upload_to="media/account/%Y/%m/%d/", null=True,
                                  blank=True, validators=[file_size, FileExtensionValidator(['png', 'jpeg', 'jpg'])])
    suruculuk_vesiqesi = models.ImageField(upload_to="media/account/%Y/%m/%d/", null=True, blank=True, validators=[
                                              file_size, FileExtensionValidator(['png', 'jpeg', 'jpg'])])
    department = models.ForeignKey(
        "company.Department", on_delete=models.SET_NULL, related_name="ishci", null=True, blank=True)
    shirket = models.ForeignKey(
        "company.Shirket", on_delete=models.SET_NULL, related_name="ishci", null=True, blank=True)
    ofis = models.ForeignKey("company.Ofis", on_delete=models.SET_NULL,
                             related_name="ishci", null=True, blank=True)
    shobe = models.ForeignKey("company.Shobe", on_delete=models.SET_NULL,
                              related_name="ishci", null=True, blank=True)
    vezife = models.ForeignKey(
        "company.Vezifeler", on_delete=models.SET_NULL, related_name="user_vezife", null=True)
    komanda = models.OneToOneField("company.Komanda", default=None,
                                   on_delete=models.SET_NULL, related_name="user_komanda", null=True, blank=True)
    isci_status = models.ForeignKey(
        IsciStatus, on_delete=models.SET_NULL, null=True, blank=True)
    maas_uslubu = models.CharField(
        max_length=50,
        choices=SALARY_STYLE_CHOICES,
        default=MONTHLY
    )
    muqavile_novu = models.CharField(
        max_length=50,
        choices=CONTRACT_TYPE_CHOICES,
        default=None,
        null=True,
        blank=True
    )
    maas = models.FloatField(default=0, null=True, blank=True)
    qeyd = models.TextField(null=True, blank=True)
    profile_image = models.ImageField(upload_to="media/profile/%Y/%m/%d/", null=True,
                                      blank=True, validators=[file_size, FileExtensionValidator(['png', 'jpeg', 'jpg'])])
    supervisor = models.ForeignKey(
        "self", on_delete=models.SET_NULL, null=True, blank=True, related_name="employees")

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        ordering = ("pk",)
        default_permissions = []
        permissions = (
            ("view_user", "Mövcud işçilərə baxa bilər"),
            ("add_user", "İşçi əlavə edə bilər"),
            ("change_user", "İşçi məlumatlarını yeniləyə bilər"),
            ("delete_user", "İşçi silə bilər")
        )

    # def __str__(self):
    #     return f"{self.username}"


class Bolge(models.Model):
    bolge_adi = models.CharField(max_length=300, unique=True)

    class Meta:
        ordering = ("pk",)
        default_permissions = []
        permissions = (
            ("view_bolge", "Mövcud bölgələrə baxa bilər"),
            ("add_bolge", "Bölgə əlavə edə bilər"),
            ("change_bolge", "Bölgə məlumatlarını yeniləyə bilər"),
            ("delete_bolge", "Bölgə silə bilər")
        )

    # def __str__(self) -> str:
    #     return self.bolge_adi


class Musteri(models.Model):
    asa = models.CharField(max_length=200)
    email = models.EmailField(null=True, blank=True)
    profile_image = models.ImageField(upload_to="media/%Y/%m/%d/", null=True, blank=True, validators=[
                                      file_size, FileExtensionValidator(['png', 'jpeg', 'jpg'])])
    sv_image = models.ImageField(upload_to="media/%Y/%m/%d/", null=True, blank=True,
                                 validators=[file_size, FileExtensionValidator(['png', 'jpeg', 'jpg'])])
    sv_image2 = models.ImageField(upload_to="media/%Y/%m/%d/", null=True, blank=True,
                                  validators=[file_size, FileExtensionValidator(['png', 'jpeg', 'jpg'])])
    tel1 = models.CharField(max_length=50)
    tel2 = models.CharField(max_length=50, null=True, blank=True)
    tel3 = models.CharField(max_length=50, null=True, blank=True)
    tel4 = models.CharField(max_length=50, null=True, blank=True)
    unvan = models.TextField(blank=True)
    bolge = models.ForeignKey(Bolge, on_delete=models.SET_NULL, null=True)
    qeyd = models.TextField(blank=True)
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )

    class Meta:
        ordering = ("pk",)
        default_permissions = []
        permissions = (
            ("view_musteri", "Mövcud müştərilərə baxa bilər"),
            ("add_musteri", "Müştəri əlavə edə bilər"),
            ("change_musteri", "Müştəri məlumatlarını yeniləyə bilər"),
            ("delete_musteri", "Müştəri silə bilər")
        )

    # def __str__(self):
    #     return self.asa


class MusteriQeydler(models.Model):
    qeyd = models.TextField()
    musteri = models.ForeignKey(
        Musteri, on_delete=models.CASCADE, related_name="musteri_qeydler")
    tarix = models.DateField(auto_now_add=True, blank=True)

    class Meta:
        ordering = ("pk",)
        default_permissions = []
        permissions = (
            ("view_musteriqeydler", "Mövcud müştəri qeydlərinə baxa bilər"),
            ("add_musteriqeydler", "Müştəri qeydi əlavə edə bilər"),
            ("change_musteriqeydler", "Müştəri qeydinin məlumatlarını yeniləyə bilər"),
            ("delete_musteriqeydler", "Müştəri qeydlərini silə bilər")
        )

    # def __str__(self):
    #     return f"{self.musteri} -- {self.qeyd[:20]}"


class IsciSatisSayi(models.Model):
    tarix = models.DateField()
    isci = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="isci_satis_sayi")
    satis_sayi = models.PositiveIntegerField(default=0, null=True)

    class Meta:
        ordering = ("pk",)
        default_permissions = []
        permissions = (
            ("view_iscisatissayi", "Mövcud işçi satış saylarına baxa bilər"),
            ("add_iscisatissayi", "İşçi satış sayı əlavə edə bilər"),
            ("change_iscisatissayi", "İşçi satış sayı məlumatlarını yeniləyə bilər"),
            ("delete_iscisatissayi", "İşçi satış sayı silə bilər")
        )

    # def __str__(self) -> str:
    #     return f"{self.isci} {self.tarix}-də {self.satis_sayi} satış etmişdir"
