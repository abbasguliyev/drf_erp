from rest_framework.exceptions import ValidationError
from transfer.models import HoldingTransfer
from cashbox.models import HoldingCashbox, CompanyCashbox

def holding_transfer_create(
    *, user = None,
    transfer_amount: float = 0,
    transfer_note: str = None,
    sending_company = None,
    receiving_company = None
) -> HoldingTransfer:
    if sending_company is None and receiving_company is None:
        raise ValidationError({"detail": "Göndərən şirkət və qəbul edən şirkət hər ikisi boş ola bilməz"})
    
    if sending_company is not None and receiving_company is not None:
        raise ValidationError({"detail": "Göndərən şirkət və qəbul edən şirkət hər ikisi eyni anda qeyd edilə bilməz"})

    holding_cashbox = HoldingCashbox.objects.filter().last()
    if holding_cashbox is None:
        raise ValidationError({"detail": "Holdinq kassa tapılmadı"})
    
    previous_balance = holding_cashbox.balance
    recipient_subsequent_balance = 0
    sender_subsequent_balance = 0
    
    if sending_company is not None:
        sending_company_cashbox = CompanyCashbox.objects.select_related('company').filter(company=sending_company).last()
        if transfer_amount > sending_company_cashbox.balance:
            raise ValidationError({"detail": "Transfer məbləği kassanın balansıdan böyük ola bilməz"})
        sender_subsequent_balance = sending_company_cashbox.balance - transfer_amount
        sending_company_cashbox.balance = sender_subsequent_balance
        sending_company_cashbox.save()

        recipient_subsequent_balance = previous_balance + transfer_amount
        holding_cashbox.balance = recipient_subsequent_balance
        holding_cashbox.save()

    if receiving_company is not None:
        receiving_company_cashbox = CompanyCashbox.objects.select_related('company').filter(company=receiving_company).last()
        if transfer_amount > previous_balance:
            raise ValidationError({"detail": "Transfer məbləği kassanın balansıdan böyük ola bilməz"})
        recipient_subsequent_balance = receiving_company_cashbox.balance + transfer_amount
        receiving_company_cashbox.balance = recipient_subsequent_balance
        receiving_company_cashbox.save()
        
        sender_subsequent_balance = previous_balance - transfer_amount
        holding_cashbox.balance = sender_subsequent_balance
        holding_cashbox.save()
        
    obj = HoldingTransfer.objects.create(
        executor = user,
        sending_company = sending_company,
        receiving_company = receiving_company,
        transfer_amount = transfer_amount,
        transfer_note = transfer_note,
        recipient_subsequent_balance = recipient_subsequent_balance,
        sender_subsequent_balance = sender_subsequent_balance
    )

    obj.full_clean()
    obj.save()
    
    return obj