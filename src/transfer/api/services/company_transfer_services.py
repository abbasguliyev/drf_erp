from rest_framework.exceptions import ValidationError
from transfer.models import CompanyTransfer
from cashbox.models import CompanyCashbox, OfficeCashbox
from cashbox.api.selectors import (
    company_cashbox_list,
    office_cashbox_list,
    cash_flow_list,
    holding_cashbox_opr_list,
    company_cashbox_opr_list
)

def company_transfer_create(
    *, user = None,
    transfer_amount: float = 0,
    transfer_note: str = None,
    company = None,
    sending_office = None,
    receiving_office = None
) -> CompanyTransfer:
    if sending_office is None and receiving_office is None:
        raise ValidationError({"detail": "Göndərən ofis və qəbul edən ofis hər ikisi boş ola bilməz"})
    
    if sending_office is not None and receiving_office is not None:
        raise ValidationError({"detail": "Göndərən ofis və qəbul edən ofis hər ikisi eyni anda qeyd edilə bilməz"})

    if company is None:
        if user.company is not None:
            company = user.company
        else:
            raise ValidationError({"detail": "Şirkət daxil edilməyib"})
    
    company_cashbox = company_cashbox_list().filter(company= company).last()
    previous_balance = company_cashbox.balance
    recipient_subsequent_balance = 0
    sender_subsequent_balance = 0
    
    if sending_office is not None:
        sending_office_cashbox = office_cashbox_list().filter(office=sending_office).last()
        if transfer_amount > sending_office_cashbox.balance:
            raise ValidationError({"detail": "Transfer məbləği kassanın balansıdan böyük ola bilməz"})
        sender_subsequent_balance = sending_office_cashbox.balance - transfer_amount
        sending_office_cashbox.balance = sender_subsequent_balance
        sending_office_cashbox.save()

        recipient_subsequent_balance = previous_balance + transfer_amount
        company_cashbox.balance = recipient_subsequent_balance
        company_cashbox.save()

    if receiving_office is not None:
        receiving_office_cashbox = office_cashbox_list().filter(office=receiving_office).last()
        if transfer_amount > previous_balance:
            raise ValidationError({"detail": "Transfer məbləği kassanın balansıdan böyük ola bilməz"})
        recipient_subsequent_balance = receiving_office_cashbox.balance + transfer_amount
        receiving_office_cashbox.balance = recipient_subsequent_balance
        receiving_office_cashbox.save()
        
        sender_subsequent_balance = previous_balance - transfer_amount
        company_cashbox.balance = sender_subsequent_balance
        company_cashbox.save()


    obj = CompanyTransfer.objects.create(
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