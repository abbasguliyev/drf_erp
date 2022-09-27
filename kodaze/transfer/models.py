from django.db import models

from django.contrib.auth import get_user_model

USER = get_user_model()

class AbstractTransfer(models.Model):
    executor = models.ForeignKey(USER, on_delete=models.CASCADE, null=True)
    transfer_amount = models.FloatField(default=0)
    transfer_date = models.DateField(auto_now=True)
    transfer_note = models.TextField(null=True, blank=True)
    remaining_amount = models.FloatField(default=0, blank=True)
    previous_balance = models.FloatField(default=0, blank=True)
    subsequent_balance = models.FloatField(default=0, blank=True)

    class Meta:
        abstract = True


class TransferFromOfficeToCompany(AbstractTransfer):
    office_cashbox = models.ForeignKey("cashbox.OfficeCashbox", on_delete=models.CASCADE,
                                   related_name="transfer_from_office_to_company")
    company_cashbox = models.ForeignKey("cashbox.CompanyCashbox", on_delete=models.CASCADE,
                                      related_name="transfer_from_office_to_company")

    class Meta:
        ordering = ("-pk",)
        default_permissions = []
        permissions = (
            ("view_transferfromofficetocompany", "Mövcud ofisdən şirkətə olan transferlərə baxa bilər"),
            ("add_transferfromofficetocompany", "Ofisdən şirkətə transfer edə bilər"),
            ("change_transferfromofficetocompany", "Ofisdən şirkətə olan transfer məlumatlarını yeniləyə bilər"),
            ("delete_transferfromofficetocompany", "Ofisdən şirkətə olan transfer məlumatlarını silə bilər")
        )


class TransferFromCompanyToOffices(AbstractTransfer):
    company_cashbox = models.ForeignKey("cashbox.CompanyCashbox", on_delete=models.CASCADE, null=True,
                                      related_name="transfer_from_company_to_offices")
    office_cashbox = models.ManyToManyField("cashbox.OfficeCashbox", related_name="transfer_from_company_to_offices")

    class Meta:
        ordering = ("-pk",)
        default_permissions = []
        permissions = (
            ("view_transferfromcompanytooffices", "Mövcud şirkətdən officelərə olan transferlərə baxa bilər"),
            ("add_transferfromcompanytooffices", "Şirkətdən officelərə transfer edə bilər"),
            ("change_transferfromcompanytooffices", "Şirkətdən officelərə olan transfer məlumatlarını yeniləyə bilər"),
            ("delete_transferfromcompanytooffices", "Şirkətdən officelərə olan transfer məlumatlarını silə bilər")
        )
        

class TransferFromCompanyToHolding(AbstractTransfer):
    company_cashbox = models.ForeignKey("cashbox.CompanyCashbox", on_delete=models.CASCADE, null=True,
                                      related_name="transfer_from_company_to_holding")
    holding_cashbox = models.ForeignKey("cashbox.HoldingCashbox", on_delete=models.CASCADE, null=True,
                                      related_name="transfer_from_company_to_holding")

    class Meta:
        ordering = ("-pk",)
        default_permissions = []
        permissions = (
            ("view_transferfromcompanytoholding", "Mövcud şirkətdən holdinqlərə olan transferlərə baxa bilər"),
            ("add_transferfromcompanytoholding", "Şirkətdən holdinqlərə transfer edə bilər"),
            ("change_transferfromcompanytoholding", "Şirkətdən holdinqlərə olan transfer məlumatlarını yeniləyə bilər"),
            ("delete_transferfromcompanytoholding", "Şirkətdən holdinqlərə olan transfer məlumatlarını silə bilər")
        )


class TransferFromHoldingToCompany(AbstractTransfer):
    holding_cashbox = models.ForeignKey("cashbox.HoldingCashbox", on_delete=models.CASCADE, null=True,
                                      related_name="transfer_from_holding_to_company")
    company_cashbox = models.ManyToManyField("cashbox.CompanyCashbox", related_name="transfer_from_holding_to_company")

    class Meta:
        ordering = ("-pk",)
        default_permissions = []
        permissions = (
            ("view_transferfromholdingtocompany", "Mövcud holdinqdən şirkətlərə olan transferlərə baxa bilər"),
            ("add_transferfromholdingtocompany", "Holdinqdən şirkətlərə transfer edə bilər"),
            ("change_transferfromholdingtocompany", "Holdinqdən şirkətlərə olan transfer məlumatlarını yeniləyə bilər"),
            ("delete_transferfromholdingtocompany", "Holdinqdən şirkətlərə olan transfer məlumatlarını silə bilər")
        )