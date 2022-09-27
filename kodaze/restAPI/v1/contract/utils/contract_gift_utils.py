from rest_framework import status

from rest_framework.response import Response
from cashbox.models import OfficeCashbox

from warehouse.models import (
    Warehouse,
    Stock
)

from restAPI.v1.contract.utils.contract_utils import (
    reduce_product_from_stock, 
    add_product_to_stock, 
    c_income, 
    expense
)
from rest_framework.generics import get_object_or_404


def gifts_create(self, request, *args, **kwargs):
    serializer = self.get_serializer(data=request.data)
    user = request.user

    if serializer.is_valid():
        product = serializer.validated_data.get("product")
        contract = serializer.validated_data.get("contract")
        group_leader = contract.group_leader
        quantity = serializer.validated_data.get("quantity")
        if quantity == None or quantity == "":
            quantity = 1

        if contract.office == None:
            office = serializer.validated_data.get("office")
            if office == None or office == "":
                return Response({"detail": "Office daxil edin"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            office = contract.office

        try:
            warehouse = get_object_or_404(Warehouse, office=office)
        except:
            return Response({"detail": "Warehouse tapılmadı"}, status=status.HTTP_400_BAD_REQUEST)

        for product in product:
            try:
                stok = get_object_or_404(Stock, warehouse=warehouse, product=product)
                reduce_product_from_stock(stok, quantity)
            except:
                return Response({"detail": "Stockda məhsul qalmayıb"}, status=status.HTTP_404_NOT_FOUND)

            if product.price > 0:
                try:
                    kassa = OfficeCashbox.objects.filter(office=office)[0]
                except:
                    return Response({"detail": "Office Kassa tapılmadı"}, status=status.HTTP_400_BAD_REQUEST)
                daxil_edilecek_amount = float(product.price)*int(quantity)
                note = f"{contract} müqviləsinə {user.fullname} tərəfindən {quantity} ədəd {product} hədiyyə verildiyi üçün, {kassa} office kassasına {daxil_edilecek_amount} AZN mədaxil edildi"
                c_income(
                    cashbox=kassa,
                    daxil_edilecek_amount=daxil_edilecek_amount,
                    group_leader=user,
                    note=note
                )

        serializer.save(office=office)
        return Response({"detail": f"Müştəri {contract.customer.fullname} ilə müqaviləyə hədiyyə təyin olundu."}, status=status.HTTP_200_OK)


def gifts_destroy(self, request, *args, **kwargs):
    serializer = self.get_serializer(data=request.data)
    gifts = self.get_object()
    user = request.user

    product_query_set = gifts.product.all()
    product = list(product_query_set)
    contract = gifts.contract
    group_leader = contract.group_leader
    warehouse = get_object_or_404(Warehouse, office=contract.office)
    quantity = gifts.quantity
    for product in product:
        office = contract.office
        if product.price > 0:
            try:
                kassa = OfficeCashbox.objects.filter(office=office)[0]
            except:
                return Response({"detail": "Office Kassa tapılmadı"}, status=status.HTTP_400_BAD_REQUEST)
            daxil_edilecek_amount = float(product.price)*int(quantity)
            if daxil_edilecek_amount > float(kassa.balance):
                return Response({"detail": "Kassanın balansında yetəri qədər məbləğ yoxdur"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                note = f"{contract} müqviləsindən {user.fullname} tərəfindən {quantity} ədəd {product} hədiyyəsi geri alındığı üçün, {kassa} office kassasından {daxil_edilecek_amount} AZN məxaric edildi"
                expense(
                    cashbox=kassa,
                    daxil_edilecek_amount=daxil_edilecek_amount,
                    group_leader=user,
                    note=note
                )
        try:
            stok = get_object_or_404(Stock, warehouse=warehouse, product=product)
            add_product_to_stock(stok, quantity)
        except:
            stok = Stock.objects.create(warehouse=warehouse, product=product, quantity=quantity)
            stok.save()
        
    gifts.delete()
    return Response({"detail": "Hədiyyə stok-a geri qaytarıldı"}, status=status.HTTP_200_OK)
