from rest_framework import status
import datetime
from rest_framework.response import Response
from cashbox.models import OfficeCashbox
from salary.models import CreditorPrim, SalaryView

from product.models import (
    Product,
)

from contract.models import (
    Contract, 
    ContractCreditor,
)

from services.models import (
    ServicePayment, 
    Service
)
from warehouse.models import (
    Warehouse, 
    Stock,
)

import traceback
import pandas as pd

from rest_framework.generics import get_object_or_404

from api.v1.contract.utils.contract_utils import c_income
from api.v1.cashbox.utils import (
    calculate_holding_total_balance, 
    cashflow_create,
    calculate_office_balance, 
)
def create_is_auto_services_when_update_service(contract, created, kartric_novu, **kwargs):
    """
        Contract imzalanarken create olan servicelerin vaxti catdiqda ve
        yerine yetirildikde avtomatik yeni servicein qurulmasina xidmet eden method
    """
    if created:
        instance=contract
        now = instance.contract_date

        month = None
        if kartric_novu == "KARTRIC6AY":
            month = '6M'
        elif kartric_novu == "KARTRIC12AY":
            month = '12M'
        elif kartric_novu == "KARTRIC18AY":
            month = '18M'
        elif kartric_novu == "KARTRIC24AY":
            month = '24M'

        d = pd.to_datetime(f"{now.year}-{now.month}-{now.day}")
        month_service = pd.date_range(start=d, periods=2, freq=month)[1]
        warehouse = get_object_or_404(Warehouse, office=instance.office)
        
        kartric = Product.objects.filter(kartric_novu=kartric_novu, company=instance.company)
        for c in kartric:
            stok = Stock.objects.filter(warehouse=warehouse, product=c)[0]
            if stok == None or stok.quantity == 0:
                return Response({"detail":f"Anbarın stokunda {c.product_name} məhsulu yoxdur"}, status=status.HTTP_404_NOT_FOUND)
        
        q = 0
        while(q<instance.product_quantity):
            for i in range(1):
                price = 0
                for j in kartric:
                    price += float(j.price)
                    
                    stok = Stock.objects.filter(warehouse=warehouse, product=j)[0]
                    stok.quantity = stok.quantity - 1
                    stok.save()
                    if (stok.quantity == 0):
                        stok.delete()

                if(now.day < 29):
                    service = Service.objects.create(
                        contract=instance,
                        service_date = f"{month_service.year}-{month_service.month}-{now.day}",
                        price=price,
                        is_auto=True
                    )
                elif(now.day == 31 or now.day == 30 or now.day == 29):
                    if(month_service.day <= now.day):
                        service = Service.objects.create(
                            contract=instance,
                            service_date = f"{month_service.year}-{month_service.month}-{month_service.day}",
                            price=price,
                            is_auto=True
                        )
                    elif(month_service.day > now.day):
                        service = Service.objects.create(
                            contract=instance,
                            service_date = f"{month_service.year}-{month_service.month}-{now.day}",
                            price=price,
                            is_auto=True
                        )
                service.product.set(kartric)
                service.save()
            q+=1

def service_create(self, request, *args, **kwargs):
    serializer = self.get_serializer(data=request.data)

    if serializer.is_valid():
        contract_id = request.data.get("contract_id")
        contract = Contract.objects.get(id=contract_id)

        installment = request.data.get("installment")

        loan_term = request.data.get("loan_term")

        if bool(installment) == True: 
            if ((int(loan_term) == 0) or (int(loan_term) == 1)):
                return Response({"detail":"Kredit statusu qeyd olunarsa, kredit müddəti 0 və ya 1 daxil edilə bilməz"}, status=status.HTTP_400_BAD_REQUEST)
        discount = serializer.validated_data.get("discount")
        if discount == None:
            discount = 0
        service_date = request.data.get("service_date")
        is_done = request.data.get("is_done")
        initial_payment = request.data.get("initial_payment")
        if initial_payment == None:
            initial_payment = 0
        
        product = []
        product_data = request.data.get("product_id")
        for meh in product_data:
            mhs = Product.objects.get(pk=int(meh))
            product.append(mhs)
        warehouse = get_object_or_404(Warehouse, office=contract.office)
        for j in product:
            try:
                stok = get_object_or_404(Stock, warehouse=warehouse, product=j)
            except Exception:
                return Response({"detail": f"Warehouseın stokunda {j.product_name} məhsulu yoxdur"}, status=status.HTTP_404_NOT_FOUND)

        price = 0
        for i in product:
            price += i.price
            try:
                stok = get_object_or_404(Stock, warehouse=warehouse, product=i)
                stok.quantity = stok.quantity - 1
                stok.save()
                if (stok.quantity == 0):
                    stok.delete()
            except Exception:
                traceback.print_exc()
                return Response({"detail":"Warehouseın stokunda məhsul yoxdur"}, status=status.HTTP_404_NOT_FOUND)

        if float(discount) >  float(price):
            return Response({"detail":"Endirim qiyməti service qiymətindən çox ola bilməz"}, status=status.HTTP_400_BAD_REQUEST)

        total_amount_to_be_paid = float(price) - float(initial_payment) - float(discount)
        
        serializer.save(total_amount_to_be_paid=total_amount_to_be_paid, price=price)
        return Response({"detail":"Service düzəldildi"}, status=status.HTTP_200_OK)
    else:
        return Response({"detail":"Məlumatları doğru daxil edin"}, status=status.HTTP_400_BAD_REQUEST)

def service_update(self, request, *args, **kwargs):
    service = self.get_object()
    serializer = self.get_serializer(service, data=request.data, partial=True)

    if serializer.is_valid():
        contract = service.contract
        office=contract.office
        service_date = serializer.validated_data.get("service_date")
        product = serializer.validated_data.get("product")
        
        installment = serializer.validated_data.get("installment")
        loan_term = serializer.validated_data.get("loan_term")
        initial_payment = serializer.validated_data.get("initial_payment")

        discount = serializer.validated_data.get("discount")

        u_is_done = serializer.validated_data.get("is_done")
        
        is_done = service.is_done

        warehouse = get_object_or_404(Warehouse, office=contract.office)

        cashbox = get_object_or_404(OfficeCashbox, office=contract.office) 
        
        user = self.request.user

        for j in service.product.all():
            try:
                stok = get_object_or_404(Stock, warehouse=warehouse, product=j)
            except Exception:
                return Response({"detail": f"Warehouseın stokunda {j.product_name} məhsulu yoxdur"}, status=status.HTTP_404_NOT_FOUND)

        if bool(u_is_done) == True:
            for i in service.product.all():
                try:
                    stok = get_object_or_404(Stock, warehouse=warehouse, product=i)
                    stok.quantity = stok.quantity - 1
                    stok.save()
                    if (stok.quantity == 0):
                        stok.delete()
                except Exception:
                    return Response({"detail":"Warehouseın stokunda məhsul yoxdur"}, status=status.HTTP_404_NOT_FOUND)

            service_paymentleri = ServicePayment.objects.filter(service=service)
            for s in service_paymentleri:
                s.is_done = True
                s.save()

                if service.is_auto == True:
                    kartric_novu = service.product.all()[0].kartric_novu
                    create_is_auto_services_when_update_service(contract=contract, created=True, kartric_novu=kartric_novu)

                initial_balance = calculate_holding_total_balance()
                office_initial_balance = calculate_office_balance(office=office)

                note = f"Creditor - {user.fullname}, müştəri - {contract.customer.fullname}, service ödənişi"
                c_income(cashbox, s.amount_to_be_paid, user, note)
                subsequent_balance = calculate_holding_total_balance()
                office_subsequent_balance = calculate_office_balance(office=office)
                cashflow_create(
                    office=contract.office,
                    company=office.company,
                    description=note,
                    initial_balance=initial_balance,
                    subsequent_balance=subsequent_balance,
                    office_initial_balance=office_initial_balance,
                    office_subsequent_balance=office_subsequent_balance,
                    executor=user,
                    operation_style="MƏDAXİL",
                    quantity=float(s.amount_to_be_paid)
                )
        serializer.save()
        return Response({"detail":"Proses yerinə yetirildi"}, status=status.HTTP_200_OK)


def service_payment_update(self, request, *args, **kwargs):
    service_payment = self.get_object()
    serializer = self.get_serializer(service_payment, data=request.data, partial=True)
    
    if serializer.is_valid():
        is_done = serializer.validated_data.get("is_done")
        contract = service_payment.service.contract
        try:
            creditor_contracts = ContractCreditor.objects.filter(contract=contract)[0]
        except:
            return Response({"detail":"Creditor təyin edilməyib"}, status=status.HTTP_400_BAD_REQUEST)
        creditor = creditor_contracts.creditor

        creditor_prim_all = CreditorPrim.objects.all()

        creditor_prim = creditor_prim_all[0]

        prim_percent = creditor_prim.prim_percent

        now = datetime.date.today()

        this_month = f"{now.year}-{now.month}-{1}"

        salary_goruntulenme_creditor = SalaryView.objects.get(employee=creditor, date=this_month)

        user = self.request.user

        cashbox = get_object_or_404(OfficeCashbox, office=contract.office) 

        if is_done is not None:
            if bool(is_done) == True:
                serviceler_qs = ServicePayment.objects.filter(service=service_payment.service, is_done=False)
                serviceler = list(serviceler_qs)
                if service_payment == serviceler[-1]:
                    service_payment.service.is_done = True
                    service_payment.service.save()
                    service_payment.is_done = True
                    service_payment.save()
                    if service_payment.service.is_auto == True:
                        kartric_novu = service_payment.service.product.all()[0].kartric_novu
                        create_is_auto_services_when_update_service(contract=contract, created=True, kartric_novu=kartric_novu)

                    initial_balance = calculate_holding_total_balance()
                    office_initial_balance = calculate_office_balance(office=contract.office)
                    
                    note = f"Creditor - {user.fullname}, müştəri - {contract.customer.fullname}, service ödənişi"
                    c_income(cashbox, service_payment.amount_to_be_paid, user, note)
                    creditorun_serviceden_alacagi_amount = (float(service_payment.amount_to_be_paid) * int(prim_percent)) / 100

                    subsequent_balance = calculate_holding_total_balance()
                    office_subsequent_balance = calculate_office_balance(office=contract.office)
                    cashflow_create(
                        office=contract.office,
                        company=contract.office.company,
                        description=note,
                        initial_balance=initial_balance,
                        subsequent_balance=subsequent_balance,
                        office_initial_balance=office_initial_balance,
                        office_subsequent_balance=office_subsequent_balance,
                        executor=user,
                        operation_style="MƏDAXİL",
                        quantity=float(service_payment.amount_to_be_paid)
                    )

                    salary_goruntulenme_creditor.final_salary = salary_goruntulenme_creditor.final_salary + creditorun_serviceden_alacagi_amount
                    salary_goruntulenme_creditor.save()
                serializer.save()
                return Response({"detail":"Service məbləği ödəndi"}, status=status.HTTP_200_OK)
        serializer.save()
        return Response({"detail":"Service Ödəmə müvəffəqiyyətlə yeniləndi"}, status=status.HTTP_200_OK)