import django
import datetime
import pandas as pd
from rest_framework.exceptions import ValidationError
from cashbox.api.decorators import cashbox_operation_decorator
from contract.models import  Installment
from contract.api.selectors import installment_list

@cashbox_operation_decorator
def finish_debt(user, installment, note=None, func_name="finish_debt"):
    """
    Kredit borcunu bağlamaq funksiyası
    """
    contract = installment.contract
    if contract.debt_finished == True:
        raise ValidationError({"detail": "Borcunuz yoxdur"})

    unpaid_installments = installment_list().filter(contract=contract, payment_status="ÖDƏNMƏYƏN")
    for unpaid_installment in unpaid_installments:
        unpaid_installment.delete()

    installment.payment_status = "ÖDƏNƏN"
    installment.is_paid = True
    installment.note = note
    installment.paid_price = contract.remaining_debt
    installment.paid_date = datetime.datetime.now()
    installment.remaining_debt = 0
    installment.save()

    contract.contract_status = "BİTMİŞ"
    contract.debt_closing_date = django.utils.timezone.now()
    contract.remaining_debt = 0
    contract.debt_finished = True
    contract.save()

def delay_installment(installment, delay_date, note=None):
    """
    Kredit borcunu gecikdirmək funksiyası
    """
    contract = installment.contract
    installment_date = installment.date    

    if delay_date is None:
        raise ValidationError({'detail': 'Tarix daxil edilməyib'})

    unpaid_installments = installment_list().filter(contract=contract, payment_status="ÖDƏNMƏYƏN")

    if installment == unpaid_installments.last():
        if delay_date < installment_date:
            raise ValidationError({"detail": "Qeyd etdiyiniz tarix keçmiş tarixdir."})

        if delay_date > installment_date:
            installment.date = delay_date
            installment.delay_status = "GECİKDİRMƏ"
            installment.note = note
            installment.remaining_debt = contract.remaining_debt
            installment.save()
    elif installment != unpaid_installments.last():
        next_month = installment_list().filter(pk = installment.id+1).first()
        next_month_date = next_month.date

        if delay_date == next_month_date:
            raise ValidationError({"detail": "Qeyd etdiyiniz tarix növbəti ayın tarixi ilə eynidir."})
        elif delay_date < installment_date:
            raise ValidationError({"detail": "Qeyd etdiyiniz tarix keçmiş tarixdir."})        
        elif delay_date > next_month_date:
            raise ValidationError({"detail": "Qeyd etdiyiniz tarix növbəti ayın tarixindən böyükdür."})
        
        installment.date = delay_date
        installment.delay_status = "GECİKDİRMƏ"
        installment.note = note
        installment.remaining_debt = contract.remaining_debt
        installment.save()

@cashbox_operation_decorator
def pay_installment(*, user, installment, func_name = "pay_installment"):
    contract = installment.contract
    unpaid_installments = installment_list().filter(contract=contract, is_paid=False, payment_status="ÖDƏNMƏYƏN")
    if unpaid_installments.count() == 1:
        if installment.last_month == True:
            contract.contract_status = "BİTMİŞ"
            contract.save()
    
    installment.payment_status = "ÖDƏNƏN"
    installment.is_paid = True
    installment.paid_price = installment.price
    installment.remaining_debt = contract.remaining_debt - installment.price
    installment.paid_date = datetime.datetime.now()
    installment.save()

    contract.remaining_debt = contract.remaining_debt - installment.paid_price
    contract.save()

def pay_total_installment(user, installments):
    for installment in installments:
        if installment.is_paid == False:
            pay_installment(user=user, installment=installment, func_name="pay_installment")

def installment_update(user, instance, **data):
    payment_status = data.get("payment_status")
    delay_status = data.get("delay_status")
    close_the_debt_status = data.get("close_the_debt_status")
    date = data.get("date")
    note = data.get("note")

    if close_the_debt_status == "BORCU BAĞLA":
        finish_debt(user=user, installment=instance, note=note, func_name="finish_debt")
    elif instance.payment_status == "ÖDƏNMƏYƏN" and delay_status == "GECİKDİRMƏ":
        delay_installment(installment=instance, note=note, delay_date=date)
    else:
        raise ValidationError({'detail': 'Məlumatları doğru daxil edin'})