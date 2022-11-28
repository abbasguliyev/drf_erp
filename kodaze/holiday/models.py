from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()
# Create your models here.


class EmployeeWorkingDay(models.Model):
    employee = models.ForeignKey(User, on_delete=models.CASCADE, related_name="working_days")
    working_days_count = models.PositiveBigIntegerField(default=0)
    date = models.DateField()

    class Meta:
        ordering = ("pk",)
        default_permissions = []
        permissions = (
            ("view_employeeworkingday", "İşçilərin iş qrafikinə baxa bilər"),
        )

class EmployeeHolidayHistory(models.Model):
    created_date = models.DateField(auto_now_add=True)
    note = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ("pk",)
        default_permissions = []
        permissions = (
            ("view_employeeholidayhistory", "Mövcud tətil tarixçələrinə baxa bilər"),
            ("change_employeeholidayhistory", "Tətil tarixçəsi məlumatlarını yeniləyə bilər"),
            ("delete_employeeholidayhistory", "Tətil tarixçəsi silə bilər")
        )

class EmployeeHoliday(models.Model):
    employee = models.ForeignKey(User, on_delete=models.CASCADE, related_name="holidays")
    history = models.ForeignKey(EmployeeHolidayHistory, on_delete=models.CASCADE, related_name="holidays")
    holiday_date = models.DateField()

    class Meta:
        ordering = ("pk",)
        default_permissions = []
        permissions = (
            ("view_employeeholiday", "Mövcud tətillərə baxa bilər"),
        )

class HolidayOperation(models.Model):
    holiday_date = models.CharField(max_length=350)
    holding = models.BooleanField(default=False)
    company = models.ForeignKey('company.Company', on_delete=models.SET_NULL, null=True, blank=True, related_name="holiday_operations")    
    office = models.ForeignKey('company.Office', on_delete=models.SET_NULL, null=True, blank=True, related_name="holiday_operations")    
    person_on_duty = models.ManyToManyField(User, related_name="person_on_duty")

    class Meta:
        ordering = ("pk",)
        default_permissions = []
        permissions = (
            ("add_holidayoperation", "Tətil əlavə etmə əməliyyatı edə bilər"),
        )

class EmployeeDayOffOperation(models.Model):
    employee = models.ManyToManyField(User)
    holiday_date = models.CharField(max_length=350)
    is_paid = models.BooleanField(default=False)
    
    class Meta:
        ordering = ("pk",)
        default_permissions = []
        permissions = (
            ("add_employeedayoffoperation", "İcazə əlavə etmə əməliyyatı edə bilər"),
        )

class EmployeeDayOffHistory(models.Model):
    created_date = models.DateField(auto_now_add=True)
    note = models.TextField(null=True, blank=True)
    is_paid = models.BooleanField(default=False)

    class Meta:
        ordering = ("pk",)
        default_permissions = []
        permissions = (
            ("view_employeedayoffhistory", "Mövcud icazə tarixçələrinə baxa bilər"),
            ("change_employeedayoffhistory", "İcazə tarixçəsi məlumatlarını yeniləyə bilər"),
            ("delete_employeedayoffhistory", "İcazə tarixçəsi silə bilər")
        )

class EmployeeDayOff(models.Model):
    employee = models.ForeignKey(User, on_delete=models.CASCADE, related_name="days_off")
    history = models.ForeignKey(EmployeeDayOffHistory, on_delete=models.CASCADE, related_name="days_off")
    day_off_date = models.DateField()
    is_paid = models.BooleanField(default=False)

    class Meta:
        ordering = ("pk",)
        default_permissions = []
        permissions = (
            ("view_employeedayoff", "Mövcud icazələrə baxa bilər"),
        )
