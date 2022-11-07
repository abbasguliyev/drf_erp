from django.db import models

from django.contrib.auth import get_user_model

USER = get_user_model()

class AbstractTransfer(models.Model):
    executor = models.ForeignKey(USER, on_delete=models.CASCADE, null=True)
    transfer_amount = models.FloatField(default=0)
    transfer_date = models.DateField(auto_now=True)
    transfer_note = models.TextField(null=True, blank=True)
    previous_balance = models.FloatField(default=0, blank=True)
    subsequent_balance = models.FloatField(default=0, blank=True)

    class Meta:
        abstract = True



class HoldingTransfer(AbstractTransfer):
    sending_company = models.ForeignKey("company.Company", on_delete=models.CASCADE, null=True, blank=True, related_name="sending_companies_in_holding_transfers")
    receiving_company = models.ForeignKey("company.Company", on_delete=models.CASCADE, null=True, blank=True, related_name="receiving_companies_in_holding_transfers")

    class Meta:
        ordering = ("-pk",)
        default_permissions = []
        permissions = (
            ("view_holdingtransfer", "Mövcud holdinq transferlərə baxa bilər"),
            ("add_holdingtransfer", "Holdinq transfer edə bilər"),
            ("change_holdingtransfer", "Holdinq transfer məlumatlarını yeniləyə bilər"),
            ("delete_holdingtransfer", "Holdinq transfer məlumatlarını silə bilər")
        )

class CompanyTransfer(AbstractTransfer):
    company = models.ForeignKey("company.Company", on_delete=models.CASCADE, related_name="company_in_company_transfer")
    sending_office = models.ForeignKey("company.Office", on_delete=models.CASCADE, null=True, blank=True, related_name="sending_offices_in_company_transfers")
    receiving_office = models.ForeignKey("company.Office", on_delete=models.CASCADE, null=True, blank=True, related_name="receiving_offices_in_company_transfers")

    class Meta:
        ordering = ("-pk",)
        default_permissions = []
        permissions = (
            ("view_companytransfer", "Mövcud şirkət transferlərə baxa bilər"),
            ("add_companytransfer", "Şirkət transfer edə bilər"),
            ("change_companytransfer", "Şirkət transfer məlumatlarını yeniləyə bilər"),
            ("delete_companytransfer", "Şirkət transfer məlumatlarını silə bilər")
        )

class OfficeTransfer(AbstractTransfer):
    company = models.ForeignKey("company.Company", on_delete=models.CASCADE, related_name="company_in_office_transfer")
    sending_office = models.ForeignKey("company.Office", on_delete=models.CASCADE, null=True, blank=True, related_name="sending_offices_in_office_transfers")
    receiving_office = models.ForeignKey("company.Office", on_delete=models.CASCADE, null=True, blank=True, related_name="receiving_offices_in_office_transfers")

    class Meta:
        ordering = ("-pk",)
        default_permissions = []
        permissions = (
            ("view_officetransfer", "Mövcud ofis transferlərə baxa bilər"),
            ("add_officetransfer", "Ofis transfer edə bilər"),
            ("change_officetransfer", "Ofis transfer məlumatlarını yeniləyə bilər"),
            ("delete_officetransfer", "Ofis transfer məlumatlarını silə bilər")
        )
