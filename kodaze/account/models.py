from django.db import models
import django
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from django.core.validators import FileExtensionValidator

from .managers import CustomUserManager
from core.image_validator import file_size

class IsciStatus(models.Model):
    status_adi = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.status_adi

class User(AbstractUser):
    PRIM = 'PRİM'
    FIX = "FİX"
    PRIM_FIX = "FİX+PRİM"

    MAAS_USLUBU_CHOICES = [
        (PRIM, "PRİM"),
        (FIX, "FİX"),
        (PRIM_FIX, "FİX+PRİM"),
    ]

    first_name = None
    last_name = None

    asa= models.CharField(max_length=200)
    dogum_tarixi= models.DateField(null=True, blank=True)
    ishe_baslama_tarixi= models.DateField(default=django.utils.timezone.now, null=True, blank=True)
    ishden_cixma_tarixi= models.DateField(default=django.utils.timezone.now, null=True)
    last_login = models.DateTimeField(auto_now = True, null=True, blank=True)
    tel1=models.CharField(max_length=200)
    tel2=models.CharField(max_length=200, null=True, blank=True)
    sv_image=models.ImageField(upload_to="media/account/%Y/%m/%d/", null=True, blank=True, validators=[file_size, FileExtensionValidator(['png', 'jpeg', 'jpg'])])
    sv_image2=models.ImageField(upload_to="media/account/%Y/%m/%d/", null=True, blank=True, validators=[file_size, FileExtensionValidator(['png', 'jpeg', 'jpg'])])
    shirket=models.ForeignKey("company.Shirket", on_delete=models.SET_NULL, related_name="ishci", null=True, blank=True)
    ofis=models.ForeignKey("company.Ofis", on_delete=models.SET_NULL, related_name="ishci", null=True, blank=True)
    shobe=models.ForeignKey("company.Shobe", on_delete=models.SET_NULL, related_name="ishci", null=True, blank=True)
    vezife = models.ForeignKey("company.Vezifeler", on_delete=models.SET_NULL, related_name="user_vezife", null=True)
    komanda = models.OneToOneField("company.Komanda", default=None, on_delete=models.SET_NULL, related_name="user_komanda", null=True, blank=True)
    isci_status = models.ForeignKey(IsciStatus, on_delete=models.SET_NULL, null=True, blank=True)
    elektron_imza = models.ImageField(upload_to="media/account/%Y/%m/%d/", null=True, blank=True, validators=[file_size, FileExtensionValidator(['png', 'jpeg', 'jpg'])])
    maas_uslubu = models.CharField(
        max_length=50,
        choices=MAAS_USLUBU_CHOICES,
        default=FIX
    )
    maas = models.FloatField(default=0, null=True, blank=True)
    qeyd = models.TextField(null=True, blank=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        ordering = ("pk",)  

    def __str__(self):
        return f"{self.username}"

class Bolge(models.Model):
    bolge_adi = models.CharField(max_length=300)

    class Meta:
        ordering = ("pk",)

    def __str__(self) -> str:
        return self.bolge_adi

class Musteri(models.Model):
    asa = models.CharField(max_length=200)
    sv_image = models.ImageField(upload_to="media/%Y/%m/%d/", null=True, blank=True, validators=[file_size, FileExtensionValidator(['png', 'jpeg', 'jpg'])])
    sv_image2 = models.ImageField(upload_to="media/%Y/%m/%d/", null=True, blank=True, validators=[file_size, FileExtensionValidator(['png', 'jpeg', 'jpg'])])
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

    def __str__(self):
        return self.asa

class MusteriQeydler(models.Model):
    qeyd=models.TextField()
    musteri=models.ForeignKey(Musteri,on_delete=models.CASCADE, related_name="musteri_qeydler")
    tarix = models.DateField(auto_now_add=True, blank=True)

    class Meta:
        ordering = ("pk",)

    def __str__(self):
        return f"{self.musteri} -- {self.qeyd[:20]}"

class IsciSatisSayi(models.Model):
    tarix = models.DateField()
    isci = models.ForeignKey(User, on_delete=models.CASCADE, related_name="isci_satis_sayi")
    satis_sayi = models.PositiveIntegerField(default=0, null=True)

    class Meta:
        ordering = ("pk",)

    def __str__(self) -> str:
        return f"{self.isci} {self.tarix}-də {self.satis_sayi} satış etmişdir"