from django.db import models
import django
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils.translation import gettext_lazy as _

from django.core.validators import FileExtensionValidator

from .managers import CustomUserManager
from core.image_validator import file_size, compress
from account import (
    REGISTER_TYPE_CHOICES,
    SALARY_STYLE_CHOICES,
    COMPANY,
    FIX,
    EMPLOYEE_ACTIVITY_CHOICES,
    ACTIV
)

class EmployeeStatus(models.Model):
    status_name = models.CharField(max_length=200, unique=True)

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

class User(AbstractUser):
    first_name = None
    last_name = None

    fullname = models.CharField(max_length=200, help_text=_('Adı Soyadı Ata adı'))
    phone_number_1 = models.CharField(max_length=200, help_text=_('Telefon 1'))
    phone_number_2 = models.CharField(max_length=200, null=True, blank=True, help_text=_('Telefon 2'))
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True)
    address = models.TextField(null=True, blank=True)
    email = models.EmailField(_("email address"), null=True, blank=True)
    company = models.ForeignKey("company.Company", on_delete=models.SET_NULL, related_name="employees", null=True, blank=True, help_text=_('Şirkət'))
    office = models.ForeignKey("company.Office", on_delete=models.SET_NULL, related_name="employees", null=True, blank=True, help_text=_('Ofis'))
    department = models.ForeignKey("company.Department", on_delete=models.SET_NULL, related_name="employees", null=True, blank=True, help_text=_('Departament'))
    section = models.ForeignKey("company.Section", on_delete=models.SET_NULL, related_name="employees", null=True, blank=True, help_text=_('Şöbə'))
    supervisor = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True, related_name="employees", help_text=_('Supervizor'))
    position = models.ForeignKey("company.Position", on_delete=models.SET_NULL, related_name="employees", null=True, blank=True, help_text=_('Vəzifə'))
    photo_ID = models.ImageField(upload_to="media/account/%Y/%m/%d/", null=True, blank=True, validators=[file_size, FileExtensionValidator(['png', 'jpeg', 'jpg'])], help_text=_('Şəxsiyyət vəsiqəsi'))
    back_photo_of_ID = models.ImageField(upload_to="media/account/%Y/%m/%d/", null=True, blank=True, validators=[file_size, FileExtensionValidator(['png', 'jpeg', 'jpg'])], help_text=_('Şəxsiyyət vəsiqəsi 2'))
    driving_license_photo = models.ImageField(upload_to="media/account/%Y/%m/%d/", null=True, blank=True, validators=[file_size, FileExtensionValidator(['png', 'jpeg', 'jpg'])], help_text=_('Sürücülük vəsiqəsi'))
    employee_status = models.ForeignKey(EmployeeStatus, on_delete=models.SET_NULL, related_name="employees", null=True, blank=True, help_text=_('İşçi statusu'))
    commission = models.ForeignKey('salary.Commission', on_delete=models.SET_NULL, null=True, blank=True, related_name="employees")
    salary_style = models.CharField(
        max_length=50,
        choices=SALARY_STYLE_CHOICES,
        default=FIX
    )
    salary = models.DecimalField(default=0, max_digits=23, decimal_places=0, help_text=_('Ə/H'))
    note = models.TextField(null=True, blank=True, help_text=_('Qeyd'))
    electronic_signature = models.ImageField(upload_to="media/account/%Y/%m/%d/", null=True, blank=True, validators=[file_size, FileExtensionValidator(['png', 'jpeg', 'jpg'])])
    profile_image = models.ImageField(upload_to="media/account/%Y/%m/%d/", null=True, blank=True, validators=[file_size, FileExtensionValidator(['png', 'jpeg', 'jpg'])], help_text=_('Profil şəkli'))
    contract_date = models.DateField(auto_now_add=True)
    register_type = models.CharField(
        max_length=50,
        choices=REGISTER_TYPE_CHOICES,
        default=COMPANY,
    )
    pdf = models.FileField(upload_to="media/account/%Y/%m/%d/", blank=True, null=True, validators=[file_size, FileExtensionValidator(['pdf'])])
    fin_code = models.CharField(max_length=7, unique=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        if self.back_photo_of_ID != self.photo_ID:
            new_photo_ID = compress(self.photo_ID)
            self.photo_ID = new_photo_ID

        if self.back_photo_of_ID != None:
            new_back_photo_of_ID = compress(self.back_photo_of_ID)
            self.back_photo_of_ID = new_back_photo_of_ID
    
        if self.driving_license_photo != None:
            new_driving_license_photo = compress(self.driving_license_photo)
            self.driving_license_photo = new_driving_license_photo
        
        if self.electronic_signature != None:
            new_electronic_signature = compress(self.electronic_signature)
            self.electronic_signature = new_electronic_signature

        super().save(*args, **kwargs)

    class Meta:
        ordering = ("-pk",)
        default_permissions = []
        permissions = (
            ("view_user", "Mövcud işçilərə baxa bilər"),
            ("add_user", "İşçi əlavə edə bilər"),
            ("change_user", "İşçi məlumatlarını yeniləyə bilər"),
            ("delete_user", "İşçi silə bilər")
        )

class Customer(models.Model):
    fullname = models.CharField(max_length=200)
    email = models.EmailField(null=True, blank=True)
    phone_number_1 = models.CharField(max_length=50)
    phone_number_2 = models.CharField(max_length=50, null=True, blank=True)
    phone_number_3 = models.CharField(max_length=50, null=True, blank=True)
    phone_number_4 = models.CharField(max_length=50, null=True, blank=True)
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True)
    address = models.TextField(blank=True)
    fin_code = models.CharField(max_length=7, unique=True)
    photo_ID = models.ImageField(upload_to="media/%Y/%m/%d/", null=True, blank=True, validators=[file_size, FileExtensionValidator(['png', 'jpeg', 'jpg'])])
    back_photo_of_ID = models.ImageField(upload_to="media/%Y/%m/%d/", null=True, blank=True, validators=[file_size, FileExtensionValidator(['png', 'jpeg', 'jpg'])])
    note = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ("-pk",)
        default_permissions = []
        permissions = (
            ("view_customer", "Mövcud müştərilərə baxa bilər"),
            ("add_customer", "Müştəri əlavə edə bilər"),
            ("change_customer", "Müştəri məlumatlarını yeniləyə bilər"),
            ("delete_customer", "Müştəri silə bilər")
        )

class EmployeeActivity(models.Model):
    employee = models.ForeignKey(User, related_name="activities", on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    status = models.CharField(
        max_length=100,
        choices=EMPLOYEE_ACTIVITY_CHOICES,
        default=ACTIV
    )

    class Meta:
        ordering = ("-pk",)
        default_permissions = []
        permissions = (
            ("view_employeeactivity", "Mövcud işçi müqavilə tarixçələrinə bilər"),
            ("add_employeeactivity", "İşçi müqavilə tarixçəsi əlavə edə bilər"),
            ("change_employeeactivity", "İşçi müqavilə tarixçəsi məlumatlarını yeniləyə bilər"),
            ("delete_employeeactivity", "İşçi müqavilə tarixçəsi silə bilər")
        )