import traceback
from rest_framework import status
from rest_framework.response import Response

from warehouse.models import Stock
from rest_framework.generics import get_object_or_404
from product.api.selectors import product_list


def operation_create(self, request, *args, **kwargs):
    serializer = self.get_serializer(data=request.data)
    if serializer.is_valid():
        try:
            executor = request.user
            shipping_warehouse = serializer.validated_data.get("shipping_warehouse")
            receiving_warehouse = serializer.validated_data.get("receiving_warehouse")

            if shipping_warehouse.company != receiving_warehouse.company:
                return Response({"detail": "Əməliyyat yalnız eyni şirkətin warehouseları arasında ola bilər"}, status=status.HTTP_404_NOT_FOUND)

            product_and_quantity = serializer.validated_data.get("product_and_quantity")
            product_and_quantity_list = product_and_quantity.split(",")
            for m in product_and_quantity_list:
                product_ve_quantity = m.split("-")
                product_id = int(product_ve_quantity[0].strip())
                quantity = int(product_ve_quantity[1])
                product = product_list().filter(pk=product_id).last()
                try:
                    stok1 = get_object_or_404(
                        Stock, warehouse=shipping_warehouse, product=product)
                except:
                    return Response({"detail": "Göndərən warehouseda məhsul yoxdur"}, status=status.HTTP_404_NOT_FOUND)
                if stok1 == None:
                    return Response({"detail": "Göndərən warehouseda məhsul yoxdur"}, status=status.HTTP_404_NOT_FOUND)
                if (quantity > stok1.quantity):
                    return Response({"detail": "Göndərən warehouseda yetəri qədər məhsul yoxdur"}, status=status.HTTP_404_NOT_FOUND)
                try:
                    stok2 = get_object_or_404(
                        Stock, warehouse=receiving_warehouse, product=product)
                    if (stok1 == stok2):
                        return Response({"detail": "Göndərən və göndərilən warehouse eynidir!"}, status=status.HTTP_404_NOT_FOUND)
                    stok1.quantity = stok1.quantity - quantity
                    stok1.save()
                    if (stok1.quantity == 0):
                        stok1.delete()
                    stok2.quantity = stok2.quantity + quantity
                    stok2.save()
                    if (serializer.is_valid()):
                        serializer.save(
                            executor=executor, shipping_warehouse=shipping_warehouse, quantity=None, operation_type="transfer")
                except:
                    stok2 = Stock.objects.create(
                        warehouse=receiving_warehouse, product=product, quantity=quantity)
                    if (stok1 == stok2):
                        return Response({"detail": "Göndərən və göndərilən warehouse eynidir!"}, status=status.HTTP_404_NOT_FOUND)
                    stok2.save()
                    stok1.quantity = stok1.quantity - quantity
                    stok1.save()
                    if (serializer.is_valid()):
                        serializer.save(
                            executor=executor, shipping_warehouse=shipping_warehouse, quantity=None, operation_type="transfer")
        except:
            traceback.print_exc()
        return Response({"detail": "Əməliyyat uğurla yerinə yetirildi"}, status=status.HTTP_200_OK)
    else:
        return Response({"detail": "Məlumatları doğru daxil edin"}, status=status.HTTP_404_NOT_FOUND)
