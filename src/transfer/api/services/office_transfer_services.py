from rest_framework.exceptions import ValidationError
from transfer.models import OfficeTransfer
from cashbox.models import CompanyCashbox, OfficeCashbox
from cashbox.api.selectors import (
    office_cashbox_list,
    cash_flow_list,
    holding_cashbox_opr_list,
    company_cashbox_opr_list
)

def office_transfer_create(
    *, user = None,
    transfer_amount: float = 0,
    transfer_note: str = None,
    company,
    sending_office,
    receiving_office
) -> OfficeTransfer:
    if sending_office is None and receiving_office is None:
        raise ValidationError({"detail": "Göndərən ofis və qəbul edən ofis mütləq daxil edilməlidir"})
    
    if company is None:
        raise ValidationError({"detail": "Şirkət daxil edilməyib"})
    
    sending_office_company = sending_office.company
    receiving_office_company = receiving_office.company

    print(f"******{sending_office_company != receiving_office_company}")
    if sending_office_company != receiving_office_company:
        raise ValidationError({"detail": "Ofislər arası transfer ancaq eyni şirkətin ofisləri arasında ola bilər"})

    recipient_subsequent_balance = 0
    sender_subsequent_balance = 0
    
    sending_office_cashbox = office_cashbox_list().filter(office=sending_office).last()
    if transfer_amount > sending_office_cashbox.balance:
        raise ValidationError({"detail": "Transfer məbləği kassanın balansıdan böyük ola bilməz"})

    sender_subsequent_balance = sending_office_cashbox.balance - transfer_amount
    sending_office_cashbox.balance = sender_subsequent_balance
    sending_office_cashbox.save()

    receiving_office_cashbox = office_cashbox_list().filter(office=receiving_office).last()
    recipient_subsequent_balance = receiving_office_cashbox.balance + transfer_amount
    receiving_office_cashbox.balance = recipient_subsequent_balance
    receiving_office_cashbox.save()

    obj = OfficeTransfer.objects.create(
        executor = user,
        company=company,
        sending_office = sending_office,
        receiving_office = receiving_office,
        transfer_amount = transfer_amount,
        transfer_note = transfer_note,
        recipient_subsequent_balance = recipient_subsequent_balance,
        sender_subsequent_balance = sender_subsequent_balance
    )

    obj.full_clean()
    obj.save()
    
    return obj