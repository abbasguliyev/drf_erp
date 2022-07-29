from django.db import models

# Create your models here.
class Mehsullar(models.Model):
    KARTRIC6AY = 'KARTRIC6AY'
    KARTRIC12AY = 'KARTRIC12AY'
    KARTRIC18AY = 'KARTRIC18AY'
    KARTRIC24AY = 'KARTRIC24AY'

    KARTRIC_NOVU_CHOICES = [
        (KARTRIC6AY, "KARTRIC6AY"),
        (KARTRIC12AY, "KARTRIC12AY"),
        (KARTRIC18AY, "KARTRIC18AY"),
        (KARTRIC24AY, "KARTRIC24AY"),
    ]
    
    mehsulun_adi = models.CharField(max_length=300)
    qiymet = models.FloatField()
    shirket = models.ForeignKey('company.Shirket', on_delete=models.CASCADE, null=True, related_name="shirket_mehsul")
    is_hediyye = models.BooleanField(default=False)

    kartric_novu =  models.CharField(
        max_length=50,
        choices=KARTRIC_NOVU_CHOICES,
        default=None,
        null=True,
        blank=True
    )

    class Meta:
        ordering = ("pk",)

    def __str__(self) -> str:
        return f"{self.shirket} şirkəti {self.mehsulun_adi} - {self.qiymet} AZN"
