import traceback
from cashbox.models import OfficeCashbox
from contract.models import  Contract, Installment
import datetime
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import get_object_or_404
from warehouse.models import Warehouse, Stock
from restAPI.v1.contract.utils import contract_utils

def contract_change(self, request, *args, **kwargs):
    serializer = self.get_serializer(data=request.data)
    user = request.user

    if serializer.is_valid():
        note = serializer.validated_data.get("note")

        old_contract = serializer.validated_data.get("old_contract")
        if old_contract == None:
            return Response({"detail": "Dəyişmək istədiyiniz müqaviləni daxil edin."}, status=status.HTTP_400_BAD_REQUEST)
        payment_style = serializer.validated_data.get("payment_style")
        if payment_style == None:
            payment_style = "KREDİT"
        loan_term = serializer.validated_data.get("loan_term")
        if loan_term == None:
            return Response({"detail": "Dəyişim statusunda kredit müddəti əlavə olunmalıdır."}, status=status.HTTP_400_BAD_REQUEST)

        product = serializer.validated_data.get("product")
        if product == None:
            return Response({"detail": "Dəyişim statusunda məhsul əlavə olunmalıdır."}, status=status.HTTP_400_BAD_REQUEST)

        old_contract.modified_product_status = "DƏYİŞİLMİŞ MƏHSUL"
        old_contract.contract_status = "DÜŞƏN"
        old_contract.save()

        if payment_style == "KREDİT":
            initial_payment = old_contract.initial_payment
            if initial_payment == None:
                initial_payment = 0
            initial_payment_debt = old_contract.initial_payment_debt
            if initial_payment_debt == None:
                initial_payment_debt = 0

            paid_amount = 0

            paid_installments = Installment.objects.filter(contract = old_contract, payment_status="ÖDƏNƏN")

            if len(paid_installments) != 0:
                for odenmis_date in paid_installments:
                    paid_amount = float(paid_amount) + float(odenmis_date.price) + float(initial_payment) + float(initial_payment_debt)
            else:
                paid_amount = float(paid_amount) + float(initial_payment) + float(initial_payment_debt)

            total_amount = float(product.price) * int(old_contract.product_quantity)

            office = old_contract.office
            try:
                warehouse = get_object_or_404(Warehouse, office=office)
            except:
                return Response({"detail": "Anbar tapılmadı"}, status=status.HTTP_400_BAD_REQUEST)

            try:
                cashbox = get_object_or_404(OfficeCashbox, office=office)
            except:
                return Response({"detail": "Ofis Kassa tapılmadı"}, status=status.HTTP_400_BAD_REQUEST)

            try:
                stok = get_object_or_404(Stock, warehouse=warehouse, product=product)
            except:
                return Response({"detail": "Stokda yetəri qədər məhsul yoxdur"}, status=status.HTTP_404_NOT_FOUND)
            if (stok.quantity < int(old_contract.product_quantity)):
                return Response({"detail": "Stokda yetəri qədər məhsul yoxdur"}, status=status.HTTP_404_NOT_FOUND)

            cashbox_balance = cashbox.balance
            remaining_debt = 0

            if (int(loan_term) == 31):
                # Kredit muddeti 31 ay daxil edilerse
                return Response({"detail": "Maksimum kredit müddəti 30 aydır"}, status=status.HTTP_400_BAD_REQUEST)
            
            if (int(loan_term) == 0):
                # Kredit muddeti 0 ay daxil edilerse
                return Response({"detail": "Kredit müddəti 0 ola bilməz"}, status=status.HTTP_400_BAD_REQUEST)

            remaining_debt = float(total_amount) - float(paid_amount)
            contract_utils.reduce_product_from_stock(stok, int(old_contract.product_quantity))

            yeni_contract = Contract.objects.create(
                group_leader = old_contract.group_leader,
                manager1 = old_contract.manager1,
                manager2 = old_contract.manager2,
                customer = old_contract.customer,
                product = product,
                product_quantity = old_contract.product_quantity,
                total_amount = total_amount,
                electronic_signature = old_contract.electronic_signature,
                contract_date = datetime.date.today(),
                company = old_contract.company,
                office = old_contract.office,
                remaining_debt = remaining_debt,
                payment_style = payment_style,
                modified_product_status = "DƏYİŞİLMİŞ MƏHSUL",
                loan_term = loan_term,
                initial_payment = paid_amount,
                initial_payment_debt = 0,
                initial_payment_date = datetime.date.today(),
                initial_payment_debt_date = None,
                initial_payment_status = "BİTMİŞ",
                initial_payment_debt_status = "YOXDUR",
                cancelled_date = None,
                compensation_income = None,
                compensation_expense = None,
                note=note
            )
            yeni_contract.save()
        
        serializer.save()
        return Response({"detail": "Dəyişim yerinə yetirildi"}, status=status.HTTP_200_OK)
    else:
        traceback.print_exc()
        return Response({"detail": "Məlumatları doğru daxil edin"}, status=status.HTTP_400_BAD_REQUEST)
