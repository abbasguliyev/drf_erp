from rest_framework import status

from rest_framework.response import Response
from cashbox.models import OfficeCashbox
from contract.models import ContractGift
from product.models import Product

from warehouse.models import (
    Warehouse,
    Stock
)

from contract.api.utils.contract_utils import (
    reduce_product_from_stock, 
    add_product_to_stock, 
)
from rest_framework.generics import get_object_or_404
from cashbox.api.selectors import office_cashbox_list

def gifts_create(self, request, *args, **kwargs):
    serializer = self.get_serializer(data=request.data)
    user = request.user

    if serializer.is_valid():
        product_and_quantity = serializer.validated_data.get("products_and_quantity")
        product_and_quantity_list = product_and_quantity.split(",")
        for p in product_and_quantity_list:
            p_q = p.split("-")
            product_id = int(p_q[0].strip())
            quantity = int(p_q[1])
            product = Product.objects.get(pk=product_id)

            contract = serializer.validated_data.get("contract")
            if quantity == None or quantity == "":
                quantity = 1

            office = contract.office

            try:
                warehouse = get_object_or_404(Warehouse, office=office)
            except:
                return Response({"detail": "Anbar tapılmadı"}, status=status.HTTP_400_BAD_REQUEST)

            stok = get_object_or_404(Stock, warehouse=warehouse, product=product)
            reduce_product_from_stock(stok, quantity)
            
            if product.price > 0:
                try:
                    cashbox = office_cashbox_list().filter(office=office)[0]
                except:
                    return Response({"detail": "Ofis Kassa tapılmadı"}, status=status.HTTP_400_BAD_REQUEST)
                amount_to_be_added = float(product.price)*int(quantity)
                note = f"{contract} müqviləsinə {user.fullname} tərəfindən {quantity} ədəd {product} hədiyyə verildiyi üçün, {cashbox} ofis kassasına {amount_to_be_added} AZN mədaxil edildi"
                # c_income(
                #     company_cashbox=cashbox,
                #     the_amount_to_enter=amount_to_be_added,
                #     responsible_employee_1=user,
                #     note=note
                # )

            gift = ContractGift.objects.create(product=product, contract=contract, quantity=quantity)
            gift.save()
        return Response({"detail": f"Müştəri {contract.customer.fullname} müqaviləsinə hədiyyə əlavə edildi."}, status=status.HTTP_200_OK)


def gifts_destroy(self, request, *args, **kwargs):
    serializer = self.get_serializer(data=request.data)
    gifts = self.get_object()
    user = request.user

    product = gifts.product
    contract = gifts.contract
    group_leader = contract.group_leader
    warehouse = get_object_or_404(Warehouse, office=contract.office)
    quantity = gifts.quantity
    office = contract.office
    if product is not None:
        if product.price > 0:
            try:
                cashbox = office_cashbox_list().filter(office=office)[0]
            except:
                return Response({"detail": "Office Kassa tapılmadı"}, status=status.HTTP_400_BAD_REQUEST)
            amount_to_be_added = float(product.price)*int(quantity)
            if amount_to_be_added > float(cashbox.balance):
                return Response({"detail": "Kassanın balansında yetəri qədər məbləğ yoxdur"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                note = f"{contract} müqviləsindən {user.fullname} tərəfindən {quantity} ədəd {product} hədiyyəsi geri alındığı üçün, {cashbox} office kassasından {amount_to_be_added} AZN məxaric edildi"
                # expense(
                #     cashbox=cashbox,
                #     the_amount_to_enter=amount_to_be_added,
                #     responsible_employee_1=user,
                #     note=note
                # )
        try:
            stok = get_object_or_404(Stock, warehouse=warehouse, product=product)
            add_product_to_stock(stok, quantity)
        except:
            stok = Stock.objects.create(warehouse=warehouse, product=product, quantity=quantity)
            stok.save()
            
    gifts.delete()
    return Response({"detail": "Hədiyyə stok-a geri qaytarıldı"}, status=status.HTTP_200_OK)
