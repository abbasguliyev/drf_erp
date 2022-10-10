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

from restAPI.v1.cashbox.utils import (
    calculate_holding_total_balance, 
    cashflow_create, 
    calculate_office_balance
)

from restAPI.v1.contract.utils.contract_utils import (
    c_income, 
    expense,
    pdf_create_when_contract_updated
)

# PATCH sorgusu
def installment_patch(self, request, *args, **kwargs):
    pass

# UPDATE SORGUSU
def installment_update(self, request, *args, **kwargs):
    instance = self.get_object()
    serializer = self.get_serializer(instance, data=request.data, partial=True)
    payment_status = request.data.get("payment_status")
    conditional_payment_status = request.data.get("conditional_payment_status")
    delay_status = request.data.get("delay_status")
    natamama_gore_odeme_status = request.data.get("incomplete_month_substatus")
    sifira_gore_odeme_status = request.data.get("missed_month_substatus")
    overpayment_substatus = request.data.get('overpayment_substatus')

    user = request.user

    nowki_ay = self.get_object()
    odemek_istediyi_amount = request.data.get("price")

    if odemek_istediyi_amount == None:
        odemek_istediyi_amount = 0

    today = datetime.date.today()

    contract = nowki_ay.contract
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

    def umumi_amount(product_pricei, product_quantity):
        total_amount = product_pricei * product_quantity
        return total_amount
    
    # BORCU BAĞLA ILE BAGLI EMELIYYATLAR
    if(close_the_debt_status == "BORCU BAĞLA"):
        odenmeyen_installmentler_qs = Installment.objects.filter(contract=contract, payment_status="ÖDƏNMƏYƏN")
        odenmeyen_installmentler = list(odenmeyen_installmentler_qs)

        ay_ucun_olan_amount = 0
        for i in odenmeyen_installmentler:
            ay_ucun_olan_amount = ay_ucun_olan_amount + float(i.price)
            # i.price = 0
            # i.payment_status = "ÖDƏNƏN"
            # i.note = note
            # i.save()
            i.delete()

        nowki_ay.price = remaining_debt
        nowki_ay.payment_status = "ÖDƏNƏN"
        nowki_ay.save()

        contract.contract_status = "BİTMİŞ"
        contract.debt_closing_date = django.utils.timezone.now()
        remaining_debt = 0
        contract.remaining_debt = remaining_debt
        contract.debt_finished = True
        contract.save()

        initial_balance = calculate_holding_total_balance()
        office_initial_balance = calculate_office_balance(office=office)

        note = f"GroupLeader - {group_leader.fullname}, müştəri - {customer.fullname}, date - {today}, ödəniş üslubu - {payment_style}. Borcu tam bağlandı"
        c_income(cashbox, float(ay_ucun_olan_amount), group_leader, note)

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
            quantity=float(ay_ucun_olan_amount)
        )

        pdf_create_when_contract_updated(contract, contract, True)
        return Response({"detail": "Borc tam bağlandı"}, status=status.HTTP_200_OK)

    # GECIKDIRME ILE BAGLI EMELIYYATLAR
    if(
        (nowki_ay.payment_status == "ÖDƏNMƏYƏN" and delay_status == "GECİKDİRMƏ")  
        or 
        (nowki_ay.payment_status == "ÖDƏNMƏYƏN" and request.data.get("date") is not None) 
        or 
        (payment_status == "ÖDƏNMƏYƏN" and delay_status == "GECİKDİRMƏ") 
        or 
        (payment_status == "ÖDƏNMƏYƏN" and request.data.get("date") is not None)
    ):
        my_time = datetime.datetime.min.time()

        installment_date = nowki_ay.date
        installment = datetime.datetime.combine(installment_date, my_time)
        installment_san = datetime.datetime.timestamp(installment)

        gecikdirmek_istediyi_date = request.data.get("date")
        gecikdirmek_istediyi_date_date = datetime.datetime.strptime(gecikdirmek_istediyi_date, "%d-%m-%Y")
        gecikdirmek_istediyi_date_san = datetime.datetime.timestamp(gecikdirmek_istediyi_date_date)

        odenmeyen_installmentler_qs = Installment.objects.filter(contract=contract, payment_status="ÖDƏNMƏYƏN")
        odenmeyen_installmentler = list(odenmeyen_installmentler_qs)

        if(nowki_ay == odenmeyen_installmentler[-1]):
            try:
                if(gecikdirmek_istediyi_date_san < installment_san):
                    raise ValidationError(detail={"detail": "Tarixi doğru daxil edin!"}, code=status.HTTP_400_BAD_REQUEST)
            except:
                return Response({"detail": "Qeyd etdiyiniz date keçmiş datedir."}, status=status.HTTP_400_BAD_REQUEST)

            try:
                if(installment_san < gecikdirmek_istediyi_date_san):
                    nowki_ay.date = gecikdirmek_istediyi_date
                    nowki_ay.delay_status = "GECİKDİRMƏ"
                    # nowki_ay.note = note
                    nowki_ay.save()
                    pdf_create_when_contract_updated(contract, contract, True)
                    return Response({"detail": "Əməliyyat uğurla yerinə yetirildi"}, status=status.HTTP_200_OK)
            except:
                return Response({"detail": "Yeni date hal-hazırki date ile növbəti ayın datei arasında olmalıdır"}, status=status.HTTP_400_BAD_REQUEST)
        elif(nowki_ay != odenmeyen_installmentler[-1]):
            novbeti_ay = Installment.objects.get(pk = nowki_ay.id+1)
            novbeti_ay_date_date = novbeti_ay.date
            novbeti_ay_date = datetime.datetime.combine(novbeti_ay_date_date, my_time)
            novbeti_ay_date_san = datetime.datetime.timestamp(novbeti_ay_date)

            try:
                if(novbeti_ay_date_san == gecikdirmek_istediyi_date_san):
                    raise ValidationError(detail={"detail": "Tarixi doğru daxil edin!"}, code=status.HTTP_400_BAD_REQUEST)
            except:
                return Response({"detail": "Qeyd etdiyiniz date növbəti ayın datei ilə eynidir."}, status=status.HTTP_400_BAD_REQUEST)

            try:
                if(gecikdirmek_istediyi_date_san < installment_san):
                    raise ValidationError(detail={"detail": "Tarixi doğru daxil edin!"}, code=status.HTTP_400_BAD_REQUEST)
            except:
                return Response({"detail": "Qeyd etdiyiniz date keçmiş datedir."}, status=status.HTTP_400_BAD_REQUEST)

            try:
                if(gecikdirmek_istediyi_date_san > novbeti_ay_date_san):
                    raise ValidationError(detail={"detail": "Tarixi doğru daxil edin!"}, code=status.HTTP_400_BAD_REQUEST)
            except:
                return Response({"detail": "Qeyd etdiyiniz date növbəti ayın dateindən böyükdür."}, status=status.HTTP_400_BAD_REQUEST)

            try:
                if(installment_san < gecikdirmek_istediyi_date_san < novbeti_ay_date_san):
                    nowki_ay.date = gecikdirmek_istediyi_date
                    nowki_ay.delay_status = "GECİKDİRMƏ"
                    # nowki_ay.note = note
                    nowki_ay.save()
                    pdf_create_when_contract_updated(contract, contract, True)
                    return Response({"detail": "Əməliyyat uğurla yerinə yetirildi"}, status=status.HTTP_200_OK)
            except:
                return Response({"detail": "Yeni date hal-hazırki date ile növbəti ayın datei arasında olmalıdır"}, status=status.HTTP_400_BAD_REQUEST)
    elif(nowki_ay.payment_status != "ÖDƏNMƏYƏN" and delay_status == "GECİKDİRMƏ"):
        raise ValidationError(detail={"detail": "Gecikdirmə ancaq ödənməmiş ay üçündür"}, code=status.HTTP_400_BAD_REQUEST)
    
    # Natamam Ay odeme statusu ile bagli operationlar
    if(
        nowki_ay.payment_status == "ÖDƏNMƏYƏN" 
        and 
        conditional_payment_status == "NATAMAM AY" 
        and 
        0 < float(odemek_istediyi_amount) < nowki_ay.price 
        and 
        natamama_gore_odeme_status != ""
        and 
        natamama_gore_odeme_status is not None
    ):
        initial_payment = contract.initial_payment
        initial_payment_debt = contract.initial_payment_debt
        initial_payment_tam = initial_payment + initial_payment_debt
        productun_pricei = contract.total_amount
        nowki_ay.payment_status = "ÖDƏNƏN"
        nowki_ay.conditional_payment_status = "NATAMAM AY"
        # nowki_ay.note = note
        nowki_ay.save()


        odenmeyen_installmentler = Installment.objects.filter(contract=contract, payment_status="ÖDƏNMƏYƏN", conditional_payment_status=None)
        odemek_istediyi_amount = float(request.data.get("price"))
        
        initial_balance = calculate_holding_total_balance()
        office_initial_balance = calculate_office_balance(office=office)

        note = f"GroupLeader - {group_leader.fullname}, müştəri - {customer.fullname}, date - {today}, ödəniş üslubu - {payment_style}, şərtli ödəmə - {nowki_ay.conditional_payment_status}"
        c_income(cashbox, float(odemek_istediyi_amount), group_leader, note)
        remaining_debt = contract.remaining_debt
        remaining_debt = float(remaining_debt) - float(odemek_istediyi_amount)
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
            quantity=float(odemek_istediyi_amount)
        )
        
        if(natamama_gore_odeme_status == "NATAMAM DİGƏR AYLAR"):
            odenmeyen_pul = nowki_ay.price - odemek_istediyi_amount
            odenmeyen_aylar = len(odenmeyen_installmentler)

            buraxilmamis_odenmeyen_installmentler = Installment.objects.filter(contract=contract, payment_status="ÖDƏNMƏYƏN", conditional_payment_status=None)
            
            aylara_elave_olunacaq_amount = odenmeyen_pul // (odenmeyen_aylar - 1)
            b = aylara_elave_olunacaq_amount * (odenmeyen_aylar - 1)
            last_montha_elave_olunacaq_amount = odenmeyen_pul - b
            
            nowki_ay.price = odemek_istediyi_amount
            nowki_ay.incomplete_month_substatus = "NATAMAM DİGƏR AYLAR"
            nowki_ay.payment_status = "ÖDƏNƏN"
            # nowki_ay.note = note
            nowki_ay.save()

            i = 0
            while(i<=(odenmeyen_aylar-1)):
                if(nowki_ay == buraxilmamis_odenmeyen_installmentler[i]):
                    i+=1
                    continue
                if(i == (odenmeyen_aylar-1)):
                    odenmeyen_installmentler[i].price = odenmeyen_installmentler[i].price + last_montha_elave_olunacaq_amount
                    odenmeyen_installmentler[i].save()
                else:
                    odenmeyen_installmentler[i].price = odenmeyen_installmentler[i].price + aylara_elave_olunacaq_amount
                    odenmeyen_installmentler[i].save()
                i+=1
            if serializer.is_valid():
                serializer.save(payment_status = "ÖDƏNƏN")
                pdf_create_when_contract_updated(contract, contract, True)
                return Response({"detail": "Əməliyyat uğurla yerinə yetirildi"}, status=status.HTTP_200_OK)
            return Response({"detail": "Əməliyyat uğurla yerinə yetirildi"}, status=status.HTTP_200_OK)
        if(natamama_gore_odeme_status == "NATAMAM NÖVBƏTİ AY"):
            nowki_ay = self.get_object()
            natamam_odemek_istediyi_amount = nowki_ay.price - odemek_istediyi_amount

            novbeti_ay = get_object_or_404(Installment, pk=self.get_object().id+1)
            novbeti_ay.price = novbeti_ay.price + natamam_odemek_istediyi_amount
            novbeti_ay.save()

            nowki_ay.price = odemek_istediyi_amount
            nowki_ay.incomplete_month_substatus = "NATAMAM NÖVBƏTİ AY"
            nowki_ay.payment_status = "ÖDƏNƏN"
            # nowki_ay.note = note
            nowki_ay.save()
            pdf_create_when_contract_updated(contract, contract, True)
            return Response({"detail": "Əməliyyat uğurla yerinə yetirildi"}, status=status.HTTP_200_OK)
        if(natamama_gore_odeme_status == "NATAMAM SONUNCU AY"):
            nowki_ay = self.get_object()
            natamam_odemek_istediyi_amount = nowki_ay.price - odemek_istediyi_amount

            last_month = odenmeyen_installmentler[len(odenmeyen_installmentler)-1]
            last_month.price = last_month.price + natamam_odemek_istediyi_amount
            last_month.save()

            nowki_ay.price = odemek_istediyi_amount
            nowki_ay.incomplete_month_substatus = "NATAMAM SONUNCU AY"
            nowki_ay.payment_status = "ÖDƏNƏN"
            # nowki_ay.note = note
            nowki_ay.save()
            pdf_create_when_contract_updated(contract, contract, True)
            return Response({"detail": "Əməliyyat uğurla yerinə yetirildi"}, status=status.HTTP_200_OK)
        
    # Buraxilmis Ay odeme statusu ile bagli operationlar
    if((conditional_payment_status == "BURAXILMIŞ AY" and sifira_gore_odeme_status != None) or (float(odemek_istediyi_amount) == 0 and sifira_gore_odeme_status != None)):
        nowki_ay = self.get_object()
        contract = nowki_ay.contract
        initial_payment = contract.initial_payment
        initial_payment_debt = contract.initial_payment_debt
        productun_pricei = contract.total_amount
        initial_payment_tam = initial_payment + initial_payment_debt
        # nowki_ay.conditional_payment_status = "BURAXILMIŞ AY"
        # nowki_ay.save()
        odenmeyen_installmentler = Installment.objects.filter(contract=contract, payment_status="ÖDƏNMƏYƏN", conditional_payment_status=None)
        odemek_istediyi_amount = float(request.data.get("price"))
        
        if(sifira_gore_odeme_status == "SIFIR NÖVBƏTİ AY"):
            novbeti_ay = get_object_or_404(Installment, pk=self.get_object().id+1)
            novbeti_ay.price = novbeti_ay.price + nowki_ay.price
            novbeti_ay.save()
            nowki_ay.price = 0
            nowki_ay.conditional_payment_status = "BURAXILMIŞ AY"
            nowki_ay.missed_month_substatus = "SIFIR NÖVBƏTİ AY"
            # nowki_ay.note = note
            nowki_ay.save()
            pdf_create_when_contract_updated(contract, contract, True)
            return Response({"detail": "Əməliyyat uğurla yerinə yetirildi"}, status=status.HTTP_200_OK)
        elif(sifira_gore_odeme_status == "SIFIR SONUNCU AY"):
            last_month = odenmeyen_installmentler[len(odenmeyen_installmentler)-1]
            last_month.price = last_month.price + nowki_ay.price
            last_month.save()
            nowki_ay.price = 0
            nowki_ay.conditional_payment_status = "BURAXILMIŞ AY"
            nowki_ay.missed_month_substatus = "SIFIR SONUNCU AY"
            # nowki_ay.note = note
            nowki_ay.save()
            pdf_create_when_contract_updated(contract, contract, True)
            return Response({"detail": "Əməliyyat uğurla yerinə yetirildi"}, status=status.HTTP_200_OK)
        elif(sifira_gore_odeme_status == "SIFIR DİGƏR AYLAR"):
            odenmeyen_pul = nowki_ay.price
            buraxilmamis_odenmeyen_installmentler = Installment.objects.filter(contract=contract, payment_status="ÖDƏNMƏYƏN", conditional_payment_status=None)
            odenmeyen_aylar = len(buraxilmamis_odenmeyen_installmentler)
            aylara_elave_olunacaq_amount = odenmeyen_pul // (odenmeyen_aylar - 1)
            a = aylara_elave_olunacaq_amount * ((odenmeyen_aylar - 1)-1)
            last_montha_elave_olunacaq_amount = odenmeyen_pul - a
            nowki_ay.price = 0
            nowki_ay.conditional_payment_status = "BURAXILMIŞ AY"
            nowki_ay.missed_month_substatus = "SIFIR DİGƏR AYLAR"
            # nowki_ay.note = note
            nowki_ay.save()
            i = 0
            
            while(i<=(odenmeyen_aylar-1)):
                if(nowki_ay == buraxilmamis_odenmeyen_installmentler[i]):
                    i+=1
                    continue
                if(i == (odenmeyen_aylar-1)):
                    buraxilmamis_odenmeyen_installmentler[i].price = buraxilmamis_odenmeyen_installmentler[i].price + last_montha_elave_olunacaq_amount
                    buraxilmamis_odenmeyen_installmentler[i].save()
                else:
                    buraxilmamis_odenmeyen_installmentler[i].price = buraxilmamis_odenmeyen_installmentler[i].price + aylara_elave_olunacaq_amount
                    buraxilmamis_odenmeyen_installmentler[i].save()
                i+=1
            pdf_create_when_contract_updated(contract, contract, True)
            return Response({"detail": "Əməliyyat uğurla yerinə yetirildi"}, status=status.HTTP_200_OK)

        pdf_create_when_contract_updated(contract, contract, True)
        return Response({"detail": "Əməliyyat uğurla yerinə yetirildi"}, status=status.HTTP_200_OK)

    # RAZILASDIRILMIS AZ ODEME ile bagli operationlar
    if(conditional_payment_status == "RAZILAŞDIRILMIŞ AZ ÖDƏMƏ"):
        odemek_istediyi_amount = float(request.data.get("price"))
        if float(nowki_ay.price) <= float(odemek_istediyi_amount):
            return Response({"detail": "Razılaşdırılmış ödəmə statusunda ödənmək istənilən məbləğ əvvəlki məbləğdən az olmalıdır"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            nowki_ay = self.get_object()
            contract = nowki_ay.contract
            buraxilmamis_odenmeyen_installmentler = Installment.objects.filter(
                contract=contract, payment_status="ÖDƏNMƏYƏN", missed_month_substatus=None, conditional_payment_status=None 
                )
            initial_payment = contract.initial_payment
            initial_payment_debt = contract.initial_payment_debt
            initial_payment_tam = initial_payment + initial_payment_debt
            productun_pricei = contract.total_amount
            nowki_ay.conditional_payment_status = "RAZILAŞDIRILMIŞ AZ ÖDƏMƏ"
            # nowki_ay.note = note
            nowki_ay.save()

            # odenmeyen_installmentler = Installment.objects.filter(contract=contract, payment_status="ÖDƏNMƏYƏN")
        
            odenmeyen_pul = nowki_ay.price - odemek_istediyi_amount
            odenmeyen_aylar = len(buraxilmamis_odenmeyen_installmentler)
            
            try:
                aylara_elave_olunacaq_amount = odenmeyen_pul // (odenmeyen_aylar - 1)
            except ZeroDivisionError:
                aylara_elave_olunacaq_amount = odenmeyen_pul // odenmeyen_aylar
            if(nowki_ay.payment_status=="ÖDƏNƏN"):
                b = aylara_elave_olunacaq_amount * ((odenmeyen_aylar-1)-1)
            elif(nowki_ay.payment_status=="ÖDƏNMƏYƏN"):
                b = aylara_elave_olunacaq_amount * ((odenmeyen_aylar)-1)
            last_montha_elave_olunacaq_amount = odenmeyen_pul - b
            
            nowki_ay.payment_status = "ÖDƏNMƏYƏN"
            nowki_ay.price = odemek_istediyi_amount
            nowki_ay.save()

            remaining_debt = float(remaining_debt) - float(nowki_ay.price)
            # contract.remaining_debt = remaining_debt
            contract.save()

            i = 0
            while(i<=(odenmeyen_aylar-1)):
                if(nowki_ay == buraxilmamis_odenmeyen_installmentler[i]):
                    i+=1
                    continue
                if(i == (odenmeyen_aylar-1)):
                    buraxilmamis_odenmeyen_installmentler[i].price = buraxilmamis_odenmeyen_installmentler[i].price + last_montha_elave_olunacaq_amount
                    buraxilmamis_odenmeyen_installmentler[i].save()
                else:
                    buraxilmamis_odenmeyen_installmentler[i].price = buraxilmamis_odenmeyen_installmentler[i].price + aylara_elave_olunacaq_amount
                    buraxilmamis_odenmeyen_installmentler[i].save()
                i+=1
            pdf_create_when_contract_updated(contract, contract, True)
            return Response({"detail": "Əməliyyat uğurla yerinə yetirildi"}, status=status.HTTP_200_OK)

    # ARTIQ ODEME ile bagli operationlar
    if(conditional_payment_status == "ARTIQ ÖDƏMƏ"):
        odenmek_istenilen_amount = request.data.get("price")
        
        if float(nowki_ay.price) >= float(odenmek_istenilen_amount):
            return Response({"detail": "Artıq ödəmə statusunda ödənmək istənilən məbləğ əvvəlki məbləğdən çox olmalıdır"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            if(overpayment_substatus == "ARTIQ BİR AY"):
                nowki_ay = self.get_object()
                contract = nowki_ay.contract
                odemek_istediyi_amount = float(request.data.get("price"))
                normalda_odenmeli_olan = nowki_ay.price

                if float(odemek_istediyi_amount) > float(contract.remaining_debt):
                    return Response({"detail": "Artıq ödəmə statusunda qalıq borcunuzdan artıq məbləğ ödəyə bilməzsiniz"}, status=status.HTTP_400_BAD_REQUEST)

                artiqdan_normalda_odenmeli_olani_cixan_ferq = odemek_istediyi_amount - normalda_odenmeli_olan
                odenmeyen_installmentler = Installment.objects.filter(contract=contract, payment_status="ÖDƏNMƏYƏN")

                nowki_ay.price = odemek_istediyi_amount
                nowki_ay.conditional_payment_status = "ARTIQ ÖDƏMƏ"
                nowki_ay.overpayment_substatus = "ARTIQ BİR AY"
                nowki_ay.save()
                
                remaining_debt = float(remaining_debt) - float(odemek_istediyi_amount)
                contract.save()

                last_month = odenmeyen_installmentler[len(odenmeyen_installmentler)-1]
                sonuncudan_bir_previus_month = odenmeyen_installmentler[len(odenmeyen_installmentler)-2]
                
                last_monthdan_qalan = last_month.price - artiqdan_normalda_odenmeli_olani_cixan_ferq
                while(artiqdan_normalda_odenmeli_olani_cixan_ferq>0):
                    if(last_month.price > artiqdan_normalda_odenmeli_olani_cixan_ferq):
                        last_month.price = last_month.price - artiqdan_normalda_odenmeli_olani_cixan_ferq
                        last_month.save()
                        artiqdan_normalda_odenmeli_olani_cixan_ferq = 0

                    elif(last_month.price == artiqdan_normalda_odenmeli_olani_cixan_ferq):
                        last_month.delete()
                        contract.loan_term = contract.loan_term - 1
                        contract.save()
                        artiqdan_normalda_odenmeli_olani_cixan_ferq = 0
                    elif(last_month.price < artiqdan_normalda_odenmeli_olani_cixan_ferq):
                        artiqdan_normalda_odenmeli_olani_cixan_ferq = artiqdan_normalda_odenmeli_olani_cixan_ferq - last_month.price
                        last_month.delete()
                        contract.loan_term = contract.loan_term - 1
                        contract.save()
                        odenmeyen_installmentler = Installment.objects.filter(contract=contract, payment_status="ÖDƏNMƏYƏN")
                        last_month = odenmeyen_installmentler[len(odenmeyen_installmentler)-1]
                        sonuncudan_bir_previus_month = odenmeyen_installmentler[len(odenmeyen_installmentler)-2]

                if(request.data.get("payment_status") == "ÖDƏNƏN"):
                    remaining_debt = float(remaining_debt) - float(odemek_istediyi_amount)
                    contract.remaining_debt = remaining_debt
                    contract.save()

                    initial_balance = calculate_holding_total_balance()
                    office_initial_balance = calculate_office_balance(office=office)
                    
                    note = f"GroupLeader - {group_leader.fullname}, müştəri - {customer.fullname}, date - {today}, ödəniş üslubu - {payment_style}. installment ödəməsi"
                    c_income(cashbox, float(odemek_istediyi_amount), group_leader, note)

                    nowki_ay.payment_status = "ÖDƏNƏN"
                    nowki_ay.save()

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
                        quantity=float(odemek_istediyi_amount)
                    )


                pdf_create_when_contract_updated(contract, contract, True)
                return Response({"detail": "Əməliyyat uğurla yerinə yetirildi"}, status=status.HTTP_200_OK)
            elif(overpayment_substatus == "ARTIQ BÜTÜN AYLAR"):
                nowki_ay = self.get_object()
                contract = nowki_ay.contract
                odemek_istediyi_amount = float(request.data.get("price"))
                normalda_odenmeli_olan = nowki_ay.price

                if float(odemek_istediyi_amount) > float(contract.remaining_debt):
                    return Response({"detail": "Artıq ödəmə statusunda qalıq borcunuzdan artıq məbləğ ödəyə bilməzsiniz"}, status=status.HTTP_400_BAD_REQUEST)

                initial_payment = contract.initial_payment
                initial_payment_debt = contract.initial_payment_debt
                initial_payment_tam = initial_payment + initial_payment_debt
                productun_pricei = contract.total_amount
                odenen_installmentler = Installment.objects.filter(contract=contract, payment_status = "ÖDƏNƏN")
                odenmeyen_installmentler = Installment.objects.filter(contract=contract, payment_status="ÖDƏNMƏYƏN", conditional_payment_status=None)
                umumi_odenmeyen_installmentler = Installment.objects.filter(contract=contract, payment_status="ÖDƏNMƏYƏN").exclude(conditional_payment_status="BURAXILMIŞ AY")
                sertli_odeme = Installment.objects.filter(contract=contract, payment_status="ÖDƏNMƏYƏN").exclude(conditional_payment_status=None)

                sertli_odemeden_gelen_amount = 0
                for s in sertli_odeme:
                    sertli_odemeden_gelen_amount += float(s.price)
                payment_dateleri = Installment.objects.filter(contract=contract)
                # odediyi = len(odenen_installmentler) * nowki_ay.price
                remaining_debt = float(contract.remaining_debt)
                yeni_remaining_debt = remaining_debt-sertli_odemeden_gelen_amount
                # cixilacaq_amount = remaining_debt -  sertli_odemeden_gelen_amount
                yeni_aylar = yeni_remaining_debt // odemek_istediyi_amount
                # silinecek_ay = len(odenmeyen_installmentler) - yeni_aylar
                silinecek_ay = len(umumi_odenmeyen_installmentler) - yeni_aylar - len(sertli_odeme)
                son_aya_elave_edilecek_amount = yeni_remaining_debt - ((yeni_aylar-1) * odemek_istediyi_amount)
                nowki_ay.price = odemek_istediyi_amount
                # nowki_ay.payment_status = "ÖDƏNƏN"
                nowki_ay.conditional_payment_status = "ARTIQ ÖDƏMƏ"
                nowki_ay.overpayment_substatus = "ARTIQ BÜTÜN AYLAR"
                # nowki_ay.note = note
                nowki_ay.save()

                remaining_debt = float(remaining_debt) - float(odemek_istediyi_amount)
                # contract.remaining_debt = remaining_debt
                contract.save()

                a = 1
                while(a <= silinecek_ay):
                    odenmeyen_installmentler[len(odenmeyen_installmentler)-1].delete()
                    odenmeyen_installmentler = Installment.objects.filter(contract=contract, payment_status="ÖDƏNMƏYƏN", conditional_payment_status=None)
                    a += 1

                b = 0
                if float(odemek_istediyi_amount) == float(remaining_debt):
                    while(b < yeni_aylar):
                        odenmeyen_installmentler[b].price = odemek_istediyi_amount
                        odenmeyen_installmentler[b].save()
                        b += 1
                elif float(odemek_istediyi_amount) < float(remaining_debt):
                    while(b < yeni_aylar):
                        if(b < yeni_aylar-1):
                            installment = odenmeyen_installmentler[b]
                            installment.price = odemek_istediyi_amount
                            installment.save()
                            b += 1
                        elif(b == yeni_aylar-1):
                            odenmeyen_installmentler[len(odenmeyen_installmentler)-1].price = son_aya_elave_edilecek_amount
                            odenmeyen_installmentler[len(odenmeyen_installmentler)-1].save()
                            b += 1
                        
                # serializer.save()
                pdf_create_when_contract_updated(contract, contract, True)
                return Response({"detail": "Əməliyyat uğurla yerinə yetirildi"}, status=status.HTTP_200_OK)
    
    # SON AYIN BOLUNMESI
    if(conditional_payment_status == "SON AYIN BÖLÜNMƏSİ"):
        nowki_ay = self.get_object()
        contract = nowki_ay.contract
        odemek_istediyi_amount = float(request.data.get("price"))

        if float(odemek_istediyi_amount) == 0:
            return Response({"detail": "Sonuncu ayda 0 AZN daxil edilə bilməz"}, status=status.HTTP_400_BAD_REQUEST)

        odenmeyen_installmentler = Installment.objects.filter(contract=contract, payment_status="ÖDƏNMƏYƏN")
        last_month = odenmeyen_installmentler[len(odenmeyen_installmentler)-1]

        try:
            if(nowki_ay != last_month):
                raise ValidationError(detail={"detail": "Sonuncu ayda deyilsiniz!"}, code=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"detail": "Sonuncu ayda deyilsiniz"}, status=status.HTTP_400_BAD_REQUEST) 

        
        create_olunacaq_ay_price = last_month.price - odemek_istediyi_amount
        last_month.price = odemek_istediyi_amount
        # last_month.payment_status = "ÖDƏNƏN"
        last_month.conditional_payment_status = "SON AYIN BÖLÜNMƏSİ"
        last_month.note = note
        last_month.save()

        remaining_debt = float(remaining_debt) - float(odemek_istediyi_amount)
        # contract.remaining_debt = remaining_debt
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
    if((nowki_ay.payment_status == "ÖDƏNMƏYƏN" and float(odemek_istediyi_amount) == nowki_ay.price)):
        odenmeyen_installmentler_qs = Installment.objects.filter(contract=contract, payment_status="ÖDƏNMƏYƏN")
        odenmeyen_installmentler = list(odenmeyen_installmentler_qs)
        if serializer.is_valid():
            nowki_ay.payment_status = "ÖDƏNƏN"
            # nowki_ay.note = note
            nowki_ay.save()
            if(nowki_ay == odenmeyen_installmentler[-1]):
                contract.contract_status = "BİTMİŞ"
                contract.save()
            
            remaining_debt = float(remaining_debt) - float(odemek_istediyi_amount)
            contract.remaining_debt = remaining_debt
            contract.save()

            initial_balance = calculate_holding_total_balance()
            office_initial_balance = calculate_office_balance(office=office)
            
            note = f"GroupLeader - {group_leader.fullname}, müştəri - {customer.fullname}, date - {today}, ödəniş üslubu - {payment_style}. installment ödəməsi"
            c_income(cashbox, float(odemek_istediyi_amount), group_leader, note)

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
                quantity=float(odemek_istediyi_amount)
            )

            pdf_create_when_contract_updated(contract, contract, True)
            return Response({"detail": "Əməliyyat uğurla yerinə yetirildi"}, status=status.HTTP_200_OK)
        else:
            traceback.print_exc()
            return Response({"detail": "Xəta"}, status=status.HTTP_400_BAD_REQUEST)
            # return ValidationError(detail={"detail": "Məlumatları doğru daxil edin"}, code=status.HTTP_400_BAD_REQUEST)
            
    else:
        traceback.print_exc()
        return Response({"detail": "Yanlış əməliyyat"}, status=status.HTTP_400_BAD_REQUEST)