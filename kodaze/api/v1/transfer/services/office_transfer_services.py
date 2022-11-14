from rest_framework.exceptions import ValidationError
from transfer.models import OfficeTransfer
from cashbox.models import CompanyCashbox, OfficeCashbox

def office_transfer_create(
    *, user = None,
    transfer_amount: float = 0,
    transfer_note: str = None,
    company,
    sending_office = None,
    receiving_office = None
) -> OfficeTransfer:
    if sending_office is None or receiving_office is None:
        raise ValidationError({"detail": "Göndərən ofis və qəbul edən ofis mütləq daxil edilməlidir"})
    
    if sending_office is not None and receiving_office is not None:
        raise ValidationError({"detail": "Göndərən ofis və qəbul edən ofis hər ikisi eyni anda qeyd edilə bilməz"})

    if company is None:
        raise ValidationError({"detail": "Şirkət daxil edilməyib"})
    
    sending_office_company = sending_office.company
    receiving_office_company = receiving_office.company

    print(f"******{sending_office_company != receiving_office_company}")
    if sending_office_company != receiving_office_company:
        raise ValidationError({"detail": "Ofislər arası transfer ancaq eyni şirkətin ofisləri arasında ola bilər"})

    previous_balance = 0
    subsequent_balance = 0
    
    sending_office_cashbox = OfficeCashbox.objects.select_related('office').filter(office=sending_office).last()
    if transfer_amount > sending_office_cashbox.balance:
        raise ValidationError({"detail": "Transfer məbləği kassanın balansıdan böyük ola bilməz"})
    previous_balance = sending_office_cashbox.balance

    sending_office_cashbox.balance = sending_office_cashbox.balance - transfer_amount
    sending_office_cashbox.save()
    subsequent_balance = previous_balance - transfer_amount

    receiving_office_cashbox = OfficeCashbox.objects.select_related('office').filter(office=receiving_office).last()
    receiving_office_cashbox.balance = receiving_office_cashbox.balance + transfer_amount
    receiving_office_cashbox.save()

    obj = OfficeTransfer.objects.create(
        executor = user,
        company=company,
        sending_office = sending_office,
        receiving_office = receiving_office,
        transfer_amount = transfer_amount,
        transfer_note = transfer_note,
        previous_balance = previous_balance,
        subsequent_balance = subsequent_balance
    )

    obj.full_clean()
    obj.save()
    
    return obj