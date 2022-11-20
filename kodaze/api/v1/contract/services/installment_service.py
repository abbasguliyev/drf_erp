import traceback
from cashbox.models import OfficeCashbox
from contract.models import  Installment
from rest_framework.exceptions import ValidationError
import datetime
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import get_object_or_404
import pandas as pd
import django

from api.v1.cashbox.utils import (
    calculate_holding_total_balance, 
    cashflow_create, 
    calculate_office_balance
)

from api.v1.contract.utils.contract_utils import (
    pdf_create_when_contract_updated
)

# UPDATE SORGUSU
def installment_update(self, request, *args, **kwargs):
    instance = self.get_object()
    serializer = self.get_serializer(instance, data=request.data, partial=True)
    payment_status = request.data.get("payment_status")
    conditional_payment_status = request.data.get("conditional_payment_status")
    delay_status = request.data.get("delay_status")
    incomplete_month_substatus = request.data.get("incomplete_month_substatus")
    missed_month_substatus = request.data.get("missed_month_substatus")
    overpayment_substatus = request.data.get('overpayment_substatus')

    user = request.user

    current_installment = self.get_object()
    amount_wants_to_pay = request.data.get("price")

    if amount_wants_to_pay == None:
        amount_wants_to_pay = 0

    today = datetime.date.today()

    contract = current_installment.contract
    group_leader = contract.group_leader
    customer = contract.customer
    payment_style = contract.payment_style
    office = contract.office

    cashbox = get_object_or_404(OfficeCashbox, office=office)

    close_the_debt_status = request.data.get("close_the_debt_status")

    remaining_debt = contract.remaining_debt

    note = request.data.get("note")
    if note == None:
        note = ""

    # BORCU BAĞLA ILE BAGLI EMELIYYATLAR
    if(close_the_debt_status == "BORCU BAĞLA"):
        if contract.debt_finished == True:
            return Response({"detail": "Borcunuz yoxdur"}, status=status.HTTP_400_BAD_REQUEST)

        unpaid_installments_qs = Installment.objects.filter(contract=contract, payment_status="ÖDƏNMƏYƏN")
        unpaid_installments = list(unpaid_installments_qs)

        amount_for_month = 0
        for i in unpaid_installments:
            amount_for_month = amount_for_month + float(i.price)
            i.delete()

        current_installment.price = remaining_debt
        current_installment.payment_status = "ÖDƏNƏN"
        current_installment.save()

        contract.contract_status = "BİTMİŞ"
        contract.debt_closing_date = django.utils.timezone.now()
        remaining_debt = 0
        contract.remaining_debt = remaining_debt
        contract.debt_finished = True
        contract.save()

        initial_balance = calculate_holding_total_balance()
        office_initial_balance = calculate_office_balance(office=office)

        note = f"GroupLeader - {group_leader.fullname}, müştəri - {customer.fullname}, tarix - {today}, ödəniş üslubu - {payment_style}. Borcu tam bağlandı"
        # c_income(cashbox, float(amount_for_month), group_leader, note)

        subsequent_balance = calculate_holding_total_balance()
        office_subsequent_balance = calculate_office_balance(office=office)
        cashflow_create(
            office=office,
            company=office.company,
            description=note,
            initial_balance=initial_balance,
            subsequent_balance=subsequent_balance,
            office_initial_balance=office_initial_balance,
            office_subsequent_balance=office_subsequent_balance,
            executor=user,
            operation_style="MƏDAXİL",
            quantity=float(amount_for_month)
        )

        pdf_create_when_contract_updated(contract, contract, True)
        return Response({"detail": "Borc tam bağlandı"}, status=status.HTTP_200_OK)

    # GECIKDIRME ILE BAGLI EMELIYYATLAR
    if(
        (current_installment.payment_status == "ÖDƏNMƏYƏN" and delay_status == "GECİKDİRMƏ")  
        or 
        (current_installment.payment_status == "ÖDƏNMƏYƏN" and request.data.get("date") is not None) 
        or 
        (payment_status == "ÖDƏNMƏYƏN" and delay_status == "GECİKDİRMƏ") 
        or 
        (payment_status == "ÖDƏNMƏYƏN" and request.data.get("date") is not None)
    ):
        my_time = datetime.datetime.min.time()

        installment_date = current_installment.date
        installment = datetime.datetime.combine(installment_date, my_time)
        installment_san = datetime.datetime.timestamp(installment)

        the_date_wants_to_delay = request.data.get("date")

        the_date_wants_to_delay_date = datetime.datetime.strptime(the_date_wants_to_delay, "%d-%m-%Y")
        
        the_date_wants_to_delay_san = datetime.datetime.timestamp(the_date_wants_to_delay_date)

        unpaid_installments_qs = Installment.objects.filter(contract=contract, payment_status="ÖDƏNMƏYƏN")
        unpaid_installments = list(unpaid_installments_qs)

        if(current_installment == unpaid_installments[-1]):
            try:
                if(the_date_wants_to_delay_san < installment_san):
                    raise ValidationError(detail={"detail": "Tarixi doğru daxil edin!"}, code=status.HTTP_400_BAD_REQUEST)
            except:
                return Response({"detail": "Qeyd etdiyiniz tarix keçmiş tarixdir."}, status=status.HTTP_400_BAD_REQUEST)

            try:
                if(installment_san < the_date_wants_to_delay_san):
                    current_installment.date = the_date_wants_to_delay
                    current_installment.delay_status = "GECİKDİRMƏ"
                    current_installment.save()
                    pdf_create_when_contract_updated(contract, contract, True)
                    return Response({"detail": "Əməliyyat uğurla yerinə yetirildi"}, status=status.HTTP_200_OK)
            except:
                return Response({"detail": "Yeni tarix hal-hazırki tarix ile növbəti ayın tarixi arasında olmalıdır"}, status=status.HTTP_400_BAD_REQUEST)
        elif(current_installment != unpaid_installments[-1]):
            next_month = Installment.objects.get(pk = current_installment.id+1)
            next_month_date_date = next_month.date
            next_month_date = datetime.datetime.combine(next_month_date_date, my_time)
            next_month_date_san = datetime.datetime.timestamp(next_month_date)

            try:
                if(next_month_date_san == the_date_wants_to_delay_san):
                    raise ValidationError(detail={"detail": "Tarixi doğru daxil edin!"}, code=status.HTTP_400_BAD_REQUEST)
            except:
                return Response({"detail": "Qeyd etdiyiniz tarix növbəti ayın tarixi ilə eynidir."}, status=status.HTTP_400_BAD_REQUEST)

            try:
                if(the_date_wants_to_delay_san < installment_san):
                    raise ValidationError(detail={"detail": "Tarixi doğru daxil edin!"}, code=status.HTTP_400_BAD_REQUEST)
            except:
                return Response({"detail": "Qeyd etdiyiniz tarix keçmiş tarixdir."}, status=status.HTTP_400_BAD_REQUEST)

            try:
                if(the_date_wants_to_delay_san > next_month_date_san):
                    raise ValidationError(detail={"detail": "Tarixi doğru daxil edin!"}, code=status.HTTP_400_BAD_REQUEST)
            except:
                return Response({"detail": "Qeyd etdiyiniz tarix növbəti ayın tarixindən böyükdür."}, status=status.HTTP_400_BAD_REQUEST)

            if(installment_date < the_date_wants_to_delay_date.date() < next_month_date_date):
                current_installment.date = the_date_wants_to_delay_date.date()
                current_installment.delay_status = "GECİKDİRMƏ"
                current_installment.save()
                pdf_create_when_contract_updated(contract, contract, True)
                return Response({"detail": "Əməliyyat uğurla yerinə yetirildi"}, status=status.HTTP_200_OK)
            else:
                return Response({"detail": "Yeni tarix hal-hazırki tarix ile növbəti ayın tarixi arasında olmalıdır"}, status=status.HTTP_400_BAD_REQUEST)    
    elif(current_installment.payment_status != "ÖDƏNMƏYƏN" and delay_status == "GECİKDİRMƏ"):
        return Response({"detail": "Gecikdirmə ancaq ödənməmiş ay üçündür"}, status=status.HTTP_400_BAD_REQUEST)
    
    # Natamam Ay odeme statusu ile bagli operationlar
    if(
        current_installment.payment_status == "ÖDƏNMƏYƏN" 
        and 
        conditional_payment_status == "NATAMAM AY" 
        and 
        0 < float(amount_wants_to_pay) < current_installment.price 
        and 
        incomplete_month_substatus != ""
        and 
        incomplete_month_substatus is not None
    ):
        initial_payment = contract.initial_payment
        initial_payment_debt = contract.initial_payment_debt
        current_installment.payment_status = "ÖDƏNƏN"
        current_installment.conditional_payment_status = "NATAMAM AY"
        current_installment.save()

        unpaid_installments = Installment.objects.filter(contract=contract, payment_status="ÖDƏNMƏYƏN", conditional_payment_status=None)
        amount_wants_to_pay = float(request.data.get("price"))
        
        initial_balance = calculate_holding_total_balance()
        office_initial_balance = calculate_office_balance(office=office)

        note = f"GroupLeader - {group_leader.fullname}, müştəri - {customer.fullname}, tarix - {today}, ödəniş üslubu - {payment_style}, şərtli ödəmə - {current_installment.conditional_payment_status}"
        # c_income(cashbox, float(amount_wants_to_pay), group_leader, note)
        remaining_debt = contract.remaining_debt
        remaining_debt = float(remaining_debt) - float(amount_wants_to_pay)
        contract.remaining_debt = remaining_debt
        contract.save()

        subsequent_balance = calculate_holding_total_balance()
        office_subsequent_balance = calculate_office_balance(office=office)
        cashflow_create(
            office=office,
            company=office.company,
            description=note,
            initial_balance=initial_balance,
            subsequent_balance=subsequent_balance,
            office_initial_balance=office_initial_balance,
            office_subsequent_balance=office_subsequent_balance,
            executor=user,
            operation_style="MƏDAXİL",
            quantity=float(amount_wants_to_pay)
        )
        
        if(incomplete_month_substatus == "NATAMAM DİGƏR AYLAR"):
            unpaid_amount = current_installment.price - amount_wants_to_pay
            unpaid_months = len(unpaid_installments)

            unmissed_unpaid_installments = Installment.objects.filter(contract=contract, payment_status="ÖDƏNMƏYƏN", conditional_payment_status=None)
            
            amount_to_added_months = unpaid_amount // (unpaid_months - 1)
            b = amount_to_added_months * (unpaid_months - 1)
            amount_to_added_last_month = unpaid_amount - b
            
            current_installment.price = amount_wants_to_pay
            current_installment.incomplete_month_substatus = "NATAMAM DİGƏR AYLAR"
            current_installment.payment_status = "ÖDƏNƏN"
            current_installment.save()

            i = 0
            while(i<=(unpaid_months-1)):
                if(current_installment == unmissed_unpaid_installments[i]):
                    i+=1
                    continue
                if(i == (unpaid_months-1)):
                    unpaid_installments[i].price = unpaid_installments[i].price + amount_to_added_last_month
                    unpaid_installments[i].save()
                else:
                    unpaid_installments[i].price = unpaid_installments[i].price + amount_to_added_months
                    unpaid_installments[i].save()
                i+=1
            if serializer.is_valid():
                serializer.save(payment_status = "ÖDƏNƏN")
                pdf_create_when_contract_updated(contract, contract, True)
                return Response({"detail": "Əməliyyat uğurla yerinə yetirildi"}, status=status.HTTP_200_OK)
            return Response({"detail": "Əməliyyat uğurla yerinə yetirildi"}, status=status.HTTP_200_OK)
        if(incomplete_month_substatus == "NATAMAM NÖVBƏTİ AY"):
            current_installment = self.get_object()
            natamam_amount_wants_to_pay = current_installment.price - amount_wants_to_pay

            next_month = get_object_or_404(Installment, pk=self.get_object().id+1)
            next_month.price = next_month.price + natamam_amount_wants_to_pay
            next_month.save()

            current_installment.price = amount_wants_to_pay
            current_installment.incomplete_month_substatus = "NATAMAM NÖVBƏTİ AY"
            current_installment.payment_status = "ÖDƏNƏN"
            current_installment.save()
            pdf_create_when_contract_updated(contract, contract, True)
            return Response({"detail": "Əməliyyat uğurla yerinə yetirildi"}, status=status.HTTP_200_OK)
        if(incomplete_month_substatus == "NATAMAM SONUNCU AY"):
            current_installment = self.get_object()
            natamam_amount_wants_to_pay = current_installment.price - amount_wants_to_pay

            last_month = unpaid_installments[len(unpaid_installments)-1]
            last_month.price = last_month.price + natamam_amount_wants_to_pay
            last_month.save()

            current_installment.price = amount_wants_to_pay
            current_installment.incomplete_month_substatus = "NATAMAM SONUNCU AY"
            current_installment.payment_status = "ÖDƏNƏN"
            current_installment.save()
            pdf_create_when_contract_updated(contract, contract, True)
            return Response({"detail": "Əməliyyat uğurla yerinə yetirildi"}, status=status.HTTP_200_OK)
        
    # Buraxilmis Ay odeme statusu ile bagli operationlar
    if((conditional_payment_status == "BURAXILMIŞ AY" and missed_month_substatus != None) or (float(amount_wants_to_pay) == 0 and missed_month_substatus != None)):
        current_installment = self.get_object()
        contract = current_installment.contract
        initial_payment = contract.initial_payment
        initial_payment_debt = contract.initial_payment_debt
        unpaid_installments = Installment.objects.filter(contract=contract, payment_status="ÖDƏNMƏYƏN", conditional_payment_status=None)
        amount_wants_to_pay = float(request.data.get("price"))
        
        if(missed_month_substatus == "SIFIR NÖVBƏTİ AY"):
            next_month = get_object_or_404(Installment, pk=self.get_object().id+1)
            next_month.price = next_month.price + current_installment.price
            next_month.save()
            current_installment.price = 0
            current_installment.conditional_payment_status = "BURAXILMIŞ AY"
            current_installment.missed_month_substatus = "SIFIR NÖVBƏTİ AY"
            current_installment.save()
            pdf_create_when_contract_updated(contract, contract, True)
            return Response({"detail": "Əməliyyat uğurla yerinə yetirildi"}, status=status.HTTP_200_OK)
        elif(missed_month_substatus == "SIFIR SONUNCU AY"):
            last_month = unpaid_installments[len(unpaid_installments)-1]
            last_month.price = last_month.price + current_installment.price
            last_month.save()
            current_installment.price = 0
            current_installment.conditional_payment_status = "BURAXILMIŞ AY"
            current_installment.missed_month_substatus = "SIFIR SONUNCU AY"
            current_installment.save()
            pdf_create_when_contract_updated(contract, contract, True)
            return Response({"detail": "Əməliyyat uğurla yerinə yetirildi"}, status=status.HTTP_200_OK)
        elif(missed_month_substatus == "SIFIR DİGƏR AYLAR"):
            unpaid_amount = current_installment.price
            unmissed_unpaid_installments = Installment.objects.filter(contract=contract, payment_status="ÖDƏNMƏYƏN", conditional_payment_status=None)
            unpaid_months = len(unmissed_unpaid_installments)
            amount_to_added_months = unpaid_amount // (unpaid_months - 1)
            a = amount_to_added_months * ((unpaid_months - 1)-1)
            amount_to_added_last_month = unpaid_amount - a
            current_installment.price = 0
            current_installment.conditional_payment_status = "BURAXILMIŞ AY"
            current_installment.missed_month_substatus = "SIFIR DİGƏR AYLAR"
            current_installment.save()
            i = 0
            
            while(i<=(unpaid_months-1)):
                if(current_installment == unmissed_unpaid_installments[i]):
                    i+=1
                    continue
                if(i == (unpaid_months-1)):
                    unmissed_unpaid_installments[i].price = unmissed_unpaid_installments[i].price + amount_to_added_last_month
                    unmissed_unpaid_installments[i].save()
                else:
                    unmissed_unpaid_installments[i].price = unmissed_unpaid_installments[i].price + amount_to_added_months
                    unmissed_unpaid_installments[i].save()
                i+=1
            pdf_create_when_contract_updated(contract, contract, True)
            return Response({"detail": "Əməliyyat uğurla yerinə yetirildi"}, status=status.HTTP_200_OK)

        pdf_create_when_contract_updated(contract, contract, True)
        return Response({"detail": "Əməliyyat uğurla yerinə yetirildi"}, status=status.HTTP_200_OK)

    # RAZILASDIRILMIS AZ ODEME ile bagli operationlar
    if(conditional_payment_status == "RAZILAŞDIRILMIŞ AZ ÖDƏMƏ"):
        amount_wants_to_pay = float(request.data.get("price"))
        if float(current_installment.price) <= float(amount_wants_to_pay):
            return Response({"detail": "Razılaşdırılmış ödəmə statusunda ödənmək istənilən məbləğ cari məbləğdən az olmalıdır"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            current_installment = self.get_object()
            contract = current_installment.contract
            unmissed_unpaid_installments = Installment.objects.filter(
                contract=contract, payment_status="ÖDƏNMƏYƏN", missed_month_substatus=None, conditional_payment_status=None 
                )
            initial_payment = contract.initial_payment
            initial_payment_debt = contract.initial_payment_debt
            current_installment.conditional_payment_status = "RAZILAŞDIRILMIŞ AZ ÖDƏMƏ"
            current_installment.save()

            unpaid_amount = current_installment.price - amount_wants_to_pay
            unpaid_months = len(unmissed_unpaid_installments)
            
            try:
                amount_to_added_months = unpaid_amount // (unpaid_months - 1)
            except ZeroDivisionError:
                amount_to_added_months = unpaid_amount // unpaid_months
            if(current_installment.payment_status=="ÖDƏNƏN"):
                b = amount_to_added_months * ((unpaid_months-1)-1)
            elif(current_installment.payment_status=="ÖDƏNMƏYƏN"):
                b = amount_to_added_months * ((unpaid_months)-1)
            amount_to_added_last_month = unpaid_amount - b
            
            current_installment.payment_status = "ÖDƏNMƏYƏN"
            current_installment.price = amount_wants_to_pay
            current_installment.save()

            remaining_debt = float(remaining_debt) - float(current_installment.price)
            contract.save()

            i = 0
            while(i<=(unpaid_months-1)):
                if(current_installment == unmissed_unpaid_installments[i]):
                    i+=1
                    continue
                if(i == (unpaid_months-1)):
                    unmissed_unpaid_installments[i].price = unmissed_unpaid_installments[i].price + amount_to_added_last_month
                    unmissed_unpaid_installments[i].save()
                else:
                    unmissed_unpaid_installments[i].price = unmissed_unpaid_installments[i].price + amount_to_added_months
                    unmissed_unpaid_installments[i].save()
                i+=1
            pdf_create_when_contract_updated(contract, contract, True)
            return Response({"detail": "Əməliyyat uğurla yerinə yetirildi"}, status=status.HTTP_200_OK)

    # ARTIQ ODEME ile bagli operationlar
    if(conditional_payment_status == "ARTIQ ÖDƏMƏ"):
        amount_wants_to_pay = request.data.get("price")
        
        if float(current_installment.price) >= float(amount_wants_to_pay):
            return Response({"detail": "Artıq ödəmə statusunda ödənmək istənilən məbləğ cari məbləğdən çox olmalıdır"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            if(overpayment_substatus == "ARTIQ BİR AY"):
                current_installment = self.get_object()
                contract = current_installment.contract
                amount_wants_to_pay = float(request.data.get("price"))
                amount_normally_due = current_installment.price

                if float(amount_wants_to_pay) > float(contract.remaining_debt):
                    return Response({"detail": "Artıq ödəmə statusunda qalıq borcunuzdan artıq məbləğ ödəyə bilməzsiniz"}, status=status.HTTP_400_BAD_REQUEST)

                difference_amount_wants_to_pay_and_amount_normally_due = amount_wants_to_pay - amount_normally_due
                unpaid_installments = Installment.objects.filter(contract=contract, payment_status="ÖDƏNMƏYƏN")

                current_installment.price = amount_wants_to_pay
                current_installment.conditional_payment_status = "ARTIQ ÖDƏMƏ"
                current_installment.overpayment_substatus = "ARTIQ BİR AY"
                current_installment.save()
                
                remaining_debt = float(remaining_debt) - float(amount_wants_to_pay)
                contract.save()

                last_month = unpaid_installments[len(unpaid_installments)-1]

                while(difference_amount_wants_to_pay_and_amount_normally_due>0):
                    if(last_month.price > difference_amount_wants_to_pay_and_amount_normally_due):
                        last_month.price = last_month.price - difference_amount_wants_to_pay_and_amount_normally_due
                        last_month.save()
                        difference_amount_wants_to_pay_and_amount_normally_due = 0

                    elif(last_month.price == difference_amount_wants_to_pay_and_amount_normally_due):
                        last_month.delete()
                        contract.loan_term = contract.loan_term - 1
                        contract.save()
                        difference_amount_wants_to_pay_and_amount_normally_due = 0
                    elif(last_month.price < difference_amount_wants_to_pay_and_amount_normally_due):
                        difference_amount_wants_to_pay_and_amount_normally_due = difference_amount_wants_to_pay_and_amount_normally_due - last_month.price
                        last_month.delete()
                        contract.loan_term = contract.loan_term - 1
                        contract.save()
                        unpaid_installments = Installment.objects.filter(contract=contract, payment_status="ÖDƏNMƏYƏN")
                        last_month = unpaid_installments[len(unpaid_installments)-1]

                if(request.data.get("payment_status") == "ÖDƏNƏN"):
                    remaining_debt = float(remaining_debt) - float(amount_wants_to_pay)
                    contract.remaining_debt = remaining_debt
                    contract.save()

                    initial_balance = calculate_holding_total_balance()
                    office_initial_balance = calculate_office_balance(office=office)
                    
                    note = f"GroupLeader - {group_leader.fullname}, müştəri - {customer.fullname}, tarix - {today}, ödəniş üslubu - {payment_style}. kredit ödəməsi"
                    # c_income(cashbox, float(amount_wants_to_pay), group_leader, note)

                    current_installment.payment_status = "ÖDƏNƏN"
                    current_installment.save()

                    subsequent_balance = calculate_holding_total_balance()
                    office_subsequent_balance = calculate_office_balance(office=office)
                    cashflow_create(
                        office=office,
                        company=office.company,
                        description=note,
                        initial_balance=initial_balance,
                        subsequent_balance=subsequent_balance,
                        office_initial_balance=office_initial_balance,
                        office_subsequent_balance=office_subsequent_balance,
                        executor=user,
                        operation_style="MƏDAXİL",
                        quantity=float(amount_wants_to_pay)
                    )


                pdf_create_when_contract_updated(contract, contract, True)
                return Response({"detail": "Əməliyyat uğurla yerinə yetirildi"}, status=status.HTTP_200_OK)
            elif(overpayment_substatus == "ARTIQ BÜTÜN AYLAR"):
                current_installment = self.get_object()
                contract = current_installment.contract
                amount_wants_to_pay = float(request.data.get("price"))
                amount_normally_due = current_installment.price

                if float(amount_wants_to_pay) > float(contract.remaining_debt):
                    return Response({"detail": "Artıq ödəmə statusunda qalıq borcunuzdan artıq məbləğ ödəyə bilməzsiniz"}, status=status.HTTP_400_BAD_REQUEST)

                unpaid_installments = Installment.objects.filter(contract=contract, payment_status="ÖDƏNMƏYƏN", conditional_payment_status=None)
                umumi_unpaid_installments = Installment.objects.filter(contract=contract, payment_status="ÖDƏNMƏYƏN").exclude(conditional_payment_status="BURAXILMIŞ AY")
                sertli_odeme = Installment.objects.filter(contract=contract, payment_status="ÖDƏNMƏYƏN").exclude(conditional_payment_status=None)

                sertli_odemeden_gelen_amount = 0
                for s in sertli_odeme:
                    sertli_odemeden_gelen_amount += float(s.price)
                remaining_debt = float(contract.remaining_debt)
                yeni_remaining_debt = remaining_debt-sertli_odemeden_gelen_amount
                yeni_aylar = yeni_remaining_debt // amount_wants_to_pay
                silinecek_ay = len(umumi_unpaid_installments) - yeni_aylar - len(sertli_odeme)
                son_aya_elave_edilecek_amount = yeni_remaining_debt - ((yeni_aylar-1) * amount_wants_to_pay)
                current_installment.price = amount_wants_to_pay
                current_installment.conditional_payment_status = "ARTIQ ÖDƏMƏ"
                current_installment.overpayment_substatus = "ARTIQ BÜTÜN AYLAR"
                current_installment.save()

                remaining_debt = float(remaining_debt) - float(amount_wants_to_pay)
                contract.save()

                a = 1
                while(a <= silinecek_ay):
                    unpaid_installments[len(unpaid_installments)-1].delete()
                    unpaid_installments = Installment.objects.filter(contract=contract, payment_status="ÖDƏNMƏYƏN", conditional_payment_status=None)
                    a += 1

                b = 0
                if float(amount_wants_to_pay) == float(remaining_debt):
                    while(b < yeni_aylar):
                        unpaid_installments[b].price = amount_wants_to_pay
                        unpaid_installments[b].save()
                        b += 1
                elif float(amount_wants_to_pay) < float(remaining_debt):
                    while(b < yeni_aylar):
                        if(b < yeni_aylar-1):
                            installment = unpaid_installments[b]
                            installment.price = amount_wants_to_pay
                            installment.save()
                            b += 1
                        elif(b == yeni_aylar-1):
                            unpaid_installments[len(unpaid_installments)-1].price = son_aya_elave_edilecek_amount
                            unpaid_installments[len(unpaid_installments)-1].save()
                            b += 1
                        
                # serializer.save()
                pdf_create_when_contract_updated(contract, contract, True)
                return Response({"detail": "Əməliyyat uğurla yerinə yetirildi"}, status=status.HTTP_200_OK)
    
    # SON AYIN BOLUNMESI
    if(conditional_payment_status == "SON AYIN BÖLÜNMƏSİ"):
        current_installment = self.get_object()
        contract = current_installment.contract
        amount_wants_to_pay = float(request.data.get("price"))

        if float(amount_wants_to_pay) == 0:
            return Response({"detail": "Sonuncu ayda 0 AZN daxil edilə bilməz"}, status=status.HTTP_400_BAD_REQUEST)

        unpaid_installments = Installment.objects.filter(contract=contract, payment_status="ÖDƏNMƏYƏN")
        last_month = unpaid_installments[len(unpaid_installments)-1]

        try:
            if(current_installment != last_month):
                raise ValidationError(detail={"detail": "Sonuncu ayda deyilsiniz!"}, code=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"detail": "Sonuncu ayda deyilsiniz"}, status=status.HTTP_400_BAD_REQUEST) 

        
        create_olunacaq_ay_price = last_month.price - amount_wants_to_pay
        last_month.price = amount_wants_to_pay
        last_month.conditional_payment_status = "SON AYIN BÖLÜNMƏSİ"
        last_month.note = note
        last_month.save()

        remaining_debt = float(remaining_debt) - float(amount_wants_to_pay)
        contract.save()

        inc_month = pd.date_range(last_month.date, periods = 2, freq='M')
        Installment.objects.create(
            month_no = int(last_month.month_no) + 1,
            contract = contract,
            date = f"{inc_month[1].year}-{inc_month[1].month}-{last_month.date.day}",
            price = create_olunacaq_ay_price
        ).save()
        pdf_create_when_contract_updated(contract, contract, True)
        return Response({"detail": "Əməliyyat uğurla yerinə yetirildi"}, status=status.HTTP_200_OK)
    # Odenen ay ile bagli operation
    if((current_installment.payment_status == "ÖDƏNMƏYƏN" and float(amount_wants_to_pay) == current_installment.price)):
        unpaid_installments_qs = Installment.objects.filter(contract=contract, payment_status="ÖDƏNMƏYƏN")
        unpaid_installments = list(unpaid_installments_qs)
        if serializer.is_valid():
            current_installment.payment_status = "ÖDƏNƏN"
            current_installment.save()
            if(current_installment == unpaid_installments[-1]):
                contract.contract_status = "BİTMİŞ"
                contract.save()
            
            remaining_debt = float(remaining_debt) - float(amount_wants_to_pay)
            contract.remaining_debt = remaining_debt
            contract.save()

            initial_balance = calculate_holding_total_balance()
            office_initial_balance = calculate_office_balance(office=office)
            
            note = f"GroupLeader - {group_leader.fullname}, müştəri - {customer.fullname}, tarix - {today}, ödəniş üslubu - {payment_style}. kredit ödəməsi"
            # c_income(cashbox, float(amount_wants_to_pay), group_leader, note)

            subsequent_balance = calculate_holding_total_balance()
            office_subsequent_balance = calculate_office_balance(office=office)
            cashflow_create(
                office=office,
                company=office.company,
                description=note,
                initial_balance=initial_balance,
                subsequent_balance=subsequent_balance,
                office_initial_balance=office_initial_balance,
                office_subsequent_balance=office_subsequent_balance,
                executor=user,
                operation_style="MƏDAXİL",
                quantity=float(amount_wants_to_pay)
            )

            pdf_create_when_contract_updated(contract, contract, True)
            return Response({"detail": "Əməliyyat uğurla yerinə yetirildi"}, status=status.HTTP_200_OK)
        else:
            traceback.print_exc()
            return Response({"detail": "Xəta"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        traceback.print_exc()
        return Response({"detail": "Yanlış əməliyyat"}, status=status.HTTP_400_BAD_REQUEST)