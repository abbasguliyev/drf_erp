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
    MONTHLY
)

class EmployeeStatus(models.Model):
    status_name = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.status_name

    class Meta:
        ordering = ("pk",)
        default_permissions = []
        permissions = (
            ("view_employeestatus", "Mövcud işçi statuslarına baxa bilər"),
            ("add_employeestatus", "İşçi statusu əlavə edə bilər"),
            ("change_employeestatus", "İşçi statusu məlumatlarını yeniləyə bilər"),
            ("delete_employeestatus", "İşçi statusunu silə bilər")
        )


class User(AbstractUser):
    first_name = None
    last_name = None

    fullname = models.CharField(max_length=200)
    start_date_of_work = models.DateField(default=django.utils.timezone.now, null=True, blank=True)
    dismissal_date = models.DateField(null=True, blank=True)
    phone_number_1 = models.CharField(max_length=200)
    phone_number_2 = models.CharField(max_length=200, null=True, blank=True)
    tag = models.ForeignKey('company.Tag', on_delete=models.SET_NULL, null=True, blank=True)
    photo_ID = models.ImageField(upload_to="media/account/%Y/%m/%d/", null=True, blank=True, validators=[file_size, FileExtensionValidator(['png', 'jpeg', 'jpg'])])
    back_photo_of_ID = models.ImageField(upload_to="media/account/%Y/%m/%d/", null=True, blank=True, validators=[file_size, FileExtensionValidator(['png', 'jpeg', 'jpg'])])
    driving_license_photo = models.ImageField(upload_to="media/account/%Y/%m/%d/", null=True, blank=True, validators=[file_size, FileExtensionValidator(['png', 'jpeg', 'jpg'])])
    department = models.ForeignKey("company.Department", on_delete=models.SET_NULL, related_name="employees", null=True, blank=True)
    company = models.ForeignKey("company.Company", on_delete=models.SET_NULL, related_name="employees", null=True, blank=True)
    office = models.ForeignKey("company.Office", on_delete=models.SET_NULL, related_name="employees", null=True, blank=True)
    section = models.ForeignKey("company.Section", on_delete=models.SET_NULL, related_name="employees", null=True, blank=True)
    position = models.ForeignKey("company.Position", on_delete=models.SET_NULL, related_name="employees", null=True, blank=True)
    team = models.OneToOneField("company.Team", default=None, on_delete=models.SET_NULL, related_name="employees", null=True, blank=True)
    employee_status = models.ForeignKey(EmployeeStatus, on_delete=models.SET_NULL, related_name="employees", null=True, blank=True)
    salary_style = models.CharField(
        max_length=50,
        choices=SALARY_STYLE_CHOICES,
        default=MONTHLY
    )
    contract_type = models.CharField(
        max_length=50,
        choices=CONTRACT_TYPE_CHOICES,
        default=None,
        null=True,
        blank=True
    )
    salary = models.FloatField(default=0, null=True, blank=True)
    note = models.TextField(null=True, blank=True)
    profile_image = models.ImageField(upload_to="media/profile/%Y/%m/%d/", null=True, blank=True, validators=[file_size, FileExtensionValidator(['png', 'jpeg', 'jpg'])])
    supervisor = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True, related_name="employees")

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

    def save(self, *args, **kwargs):
        last_user_id = User.objects.all().values_list('id', flat=True).last()
        self.username = f"user-{last_user_id+1}"
        super(User, self).save(*args, **kwargs)

class Region(models.Model):
    region_name = models.CharField(max_length=300, unique=True)

    class Meta:
        ordering = ("pk",)
        default_permissions = []
        permissions = (
            ("view_region", "Mövcud bölgələrə baxa bilər"),
            ("add_region", "Bölgə əlavə edə bilər"),
            ("change_region", "Bölgə məlumatlarını yeniləyə bilər"),
            ("delete_region", "Bölgə silə bilər")
        )

class Customer(models.Model):
    fullname = models.CharField(max_length=200)
    email = models.EmailField(null=True, blank=True)
    profile_image = models.ImageField(upload_to="media/%Y/%m/%d/", null=True, blank=True, validators=[file_size, FileExtensionValidator(['png', 'jpeg', 'jpg'])])
    photo_ID = models.ImageField(upload_to="media/%Y/%m/%d/", null=True, blank=True, validators=[file_size, FileExtensionValidator(['png', 'jpeg', 'jpg'])])
    back_photo_of_ID = models.ImageField(upload_to="media/%Y/%m/%d/", null=True, blank=True, validators=[file_size, FileExtensionValidator(['png', 'jpeg', 'jpg'])])
    phone_number_1 = models.CharField(max_length=50)
    phone_number_2 = models.CharField(max_length=50, null=True, blank=True)
    phone_number_3 = models.CharField(max_length=50, null=True, blank=True)
    phone_number_4 = models.CharField(max_length=50, null=True, blank=True)
    address = models.TextField(blank=True)
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True)
    note = models.TextField(null=True, blank=True)
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
            ("view_customer", "Mövcud müştərilərə baxa bilər"),
            ("add_customer", "Müştəri əlavə edə bilər"),
            ("change_customer", "Müştəri məlumatlarını yeniləyə bilər"),
            ("delete_customer", "Müştəri silə bilər")
        )

class CustomerNote(models.Model):
    note = models.TextField()
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="notes")
    date = models.DateField(auto_now_add=True, blank=True)

    class Meta:
        ordering = ("pk",)
        default_permissions = []
        permissions = (
            ("view_customernote", "Mövcud müştəri qeydlərinə baxa bilər"),
            ("add_customernote", "Müştəri qeydi əlavə edə bilər"),
            ("change_customernote", "Müştəri qeydinin məlumatlarını yeniləyə bilər"),
            ("delete_customernote", "Müştəri qeydlərini silə bilər")
        )