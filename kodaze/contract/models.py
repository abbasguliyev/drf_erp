from django.db import models
import django
from core.image_validator import file_size
from django.core.validators import FileExtensionValidator
from django.contrib.auth import get_user_model

USER = get_user_model()
# Create your models here.
class Muqavile(models.Model):
    KREDIT = 'KREDİT'
    NAGD = 'NƏĞD'

    ODENIS_USLUBU_CHOICES = [
        (NAGD, "NƏĞD"),
        (KREDIT, "KREDİT"),
    ]

    BITMIS = "BİTMİŞ"
    DAVAM_EDEN = "DAVAM EDƏN"
    DUSEN = "DÜŞƏN"
    YOXDUR = "YOXDUR"
    YENI_QRAFIK = "YENİ QRAFİK"

    YENI_QRAFIK_CHOICES = [
        (YENI_QRAFIK, "YENİ QRAFİK")
    ]

    MUQAVILE_STATUS_CHOICES = [
        (DAVAM_EDEN,"DAVAM EDƏN"),
        (BITMIS, "BİTMİŞ"),
        (DUSEN, "DÜŞƏN")
    ]

    ILKIN_ODENIS_STATUS_CHOICES = [
        (YOXDUR,"YOXDUR"),
        (BITMIS, "BİTMİŞ"),
        (DAVAM_EDEN,"DAVAM EDƏN"),   
    ]

    QALIQ_ILKIN_ODENIS_STATUS_CHOICES = [
        (YOXDUR,"YOXDUR"),
        (BITMIS, "BİTMİŞ"),
        (DAVAM_EDEN,"DAVAM EDƏN"),   
    ]

    NAGD_ODENIS_1_STATUS_CHOICES = [
        (YOXDUR,"YOXDUR"),
        (BITMIS, "BİTMİŞ"),
        (DAVAM_EDEN,"DAVAM EDƏN"),   
    ]

    NAGD_ODENIS_2_STATUS_CHOICES = [
        (YOXDUR,"YOXDUR"),
        (BITMIS, "BİTMİŞ"),
        (DAVAM_EDEN,"DAVAM EDƏN"),   
    ]

    DEYISMIS_MEHSUL = "DƏYİŞİLMİŞ MƏHSUL"

    DEYISMIS_MEHSUL_STATUS_CHOICES = [
        (DEYISMIS_MEHSUL, "DƏYİŞİLMİŞ MƏHSUL")
    ]

    group_leader = models.ForeignKey('account.User', on_delete=models.CASCADE, related_name="group_leader", null=True, blank=True)
    menecer1 = models.ForeignKey('account.User', on_delete=models.CASCADE, related_name="menecer1", null=True, blank=True)
    menecer2 = models.ForeignKey('account.User', on_delete=models.CASCADE, related_name="menecer2", null=True, blank=True)
    musteri = models.ForeignKey('account.Musteri', on_delete=models.CASCADE, related_name="musteri_muqavile", null=True,
                                blank=True)
    mehsul = models.ForeignKey("product.Mehsullar", on_delete=models.CASCADE, related_name="mehsul_muqavile", null=True,
                               blank=True)
    mehsul_sayi = models.PositiveIntegerField(default=1, blank=True)
    muqavile_umumi_mebleg = models.FloatField(default=0, blank=True)
    elektron_imza = models.ImageField(upload_to="media/muqavile/%Y/%m/%d/", null=True, blank=True, validators=[file_size, FileExtensionValidator(['png', 'jpeg', 'jpg'])])
    muqavile_tarixi = models.DateField(null=True, blank=True)
    muqavile_imzalanma_tarixi = models.DateField(auto_now_add=True)
    shirket = models.ForeignKey('company.Shirket', on_delete=models.CASCADE, related_name="muqavile", null=True, blank=True)
    ofis = models.ForeignKey('company.Ofis', on_delete=models.CASCADE, related_name="muqavile", null=True, blank=True)
    shobe = models.ForeignKey('company.Shobe', on_delete=models.CASCADE, related_name="muqavile", null=True, blank=True)
    qaliq_borc = models.FloatField(default=0, blank=True)
    is_sokuntu = models.BooleanField(default=False)

    odenis_uslubu =  models.CharField(
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
    pdf = models.FileField(upload_to="media/media/muqavile_doc/%Y/%m/%d/", blank=True, null=True, validators=[file_size, FileExtensionValidator(['pdf'])])
    pdf_elave = models.FileField(upload_to="media/media/muqavile_doc/%Y/%m/%d/", blank=True, null=True, validators=[file_size, FileExtensionValidator(['pdf'])])

    dusme_tarixi = models.DateField(null=True, blank=True)
    borc_baglanma_tarixi = models.DateField(null=True, blank=True)

    kompensasiya_medaxil = models.FloatField(default=0, null=True, blank=True)
    kompensasiya_mexaric = models.FloatField(default=0, null=True, blank=True)

    borc_baglandi = models.BooleanField(default=False, blank=True)

    class Meta:
        ordering = ("-pk",)
        default_permissions = []
        permissions = (
            ("view_muqavile", "Mövcud müqavilələrə baxa bilər"),
            ("add_muqavile", "Müqavilə əlavə edə bilər"),
            ("change_muqavile", "Müqavilə məlumatlarını yeniləyə bilər"),
            ("delete_muqavile", "Müqavilə silə bilər")
        )
        

    # def __str__(self) -> str:
    #     return f"{self.pk}. muqavile {self.musteri} - {self.mehsul}"

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

    # def __str__(self) -> str:
    #     return f"Hədiyyə --- {self.muqavile} - {self.mehsul}"

class OdemeTarix(models.Model):
    ODENEN = "ÖDƏNƏN"
    ODENMEYEN = "ÖDƏNMƏYƏN"
    
    BURAXILMIS_AY = "BURAXILMIŞ AY"
    NATAMAM_AY = "NATAMAM AY"
    RAZILASDIRILMIS_AZ_ODEME = "RAZILAŞDIRILMIŞ AZ ÖDƏMƏ"
    ARTIQ_ODEME = "ARTIQ ÖDƏMƏ"
    SON_AYIN_BOLUNMESI = "SON AYIN BÖLÜNMƏSİ"

    GECIKDIRME = "GECİKDİRMƏ"

    SIFIR_NOVBETI_AY = "SIFIR NÖVBƏTİ AY"
    SIFIR_SONUNCU_AY = "SIFIR SONUNCU AY"
    SIFIR_DIGER_AYLAR = "SIFIR DİGƏR AYLAR"

    NATAMAM_NOVBETI_AY = "NATAMAM NÖVBƏTİ AY"
    NATAMAM_SONUNCU_AY = "NATAMAM SONUNCU AY"
    NATAMAM_DIGER_AYLAR = "NATAMAM DİGƏR AYLAR"

    ARTIQ_BIR_AY = "ARTIQ BİR AY"
    ARTIQ_BUTUN_AYLAR = "ARTIQ BÜTÜN AYLAR"

    BORCU_BAGLA = "BORCU BAĞLA"

    ODEME_STATUS_CHOICES = [
        (ODENMEYEN,"ÖDƏNMƏYƏN"),
        (ODENEN, "ÖDƏNƏN"),
    ]

    SERTLI_ODEME_STATUSU = [
        (BURAXILMIS_AY, "BURAXILMIŞ AY"),
        (NATAMAM_AY, "NATAMAM AY"),
        (RAZILASDIRILMIS_AZ_ODEME, "RAZILAŞDIRILMIŞ AZ ÖDƏMƏ"),
        (ARTIQ_ODEME, "ARTIQ ÖDƏMƏ"),
        (SON_AYIN_BOLUNMESI, "SON AYIN BÖLÜNMƏSİ")
    ]

    GECIKDIRME_STATUS_CHOICES = [
        (GECIKDIRME, "GECİKDİRMƏ")
    ]

    SIFIR_STATUS_CHOICES = [
        (SIFIR_NOVBETI_AY,"SIFIR NÖVBƏTİ AY"),
        (SIFIR_SONUNCU_AY, "SIFIR SONUNCU AY"),
        (SIFIR_DIGER_AYLAR, "SIFIR DİGƏR AYLAR")
    ]

    NATAMAM_STATUS_CHOICES = [
        (NATAMAM_NOVBETI_AY,"NATAMAM NÖVBƏTİ AY"),
        (NATAMAM_SONUNCU_AY, "NATAMAM SONUNCU AY"),
        (NATAMAM_DIGER_AYLAR, "NATAMAM DİGƏR AYLAR")
    ]

    ARTIQ_ODEME_STATUS_CHOICES = [
        (ARTIQ_BIR_AY,"ARTIQ BİR AY"),
        (ARTIQ_BUTUN_AYLAR, "ARTIQ BÜTÜN AYLAR")
    ]

    BORCU_BAGLA_STATUS_CHOICES = [
        (BORCU_BAGLA,"BORCU BAĞLA")
    ]
    
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

    # def __str__(self) -> str:
    #     return f"{self.pk}. {self.ay_no}.ay-{self.tarix} - ({self.muqavile.id}) id-li muqavile - {self.muqavile.musteri.asa} - {self.qiymet}"

class Deyisim(models.Model):
    kohne_muqavile = models.ForeignKey(Muqavile, related_name="deyisim", on_delete=models.CASCADE)
    KREDIT = 'KREDİT'
    NAGD = 'NƏĞD'

    ODENIS_USLUBU_CHOICES = [
        (NAGD, "NƏĞD"),
        (KREDIT, "KREDİT"),
    ]
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

    # def __str__(self) -> str:
    #     return f"{self.user.username}-{self.count} demo - {self.created_date}"

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
    
    # def __str__(self) -> str:
    #     return f"{self.kreditor.asa} {self.muqavile}"
