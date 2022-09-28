import datetime
from rest_framework import status
from rest_framework.response import Response
from warehouse.models import Operation

def stok_update(self, request, *args, **kwargs):
    stok = self.get_object()
    serializer = self.get_serializer(stok, data=request.data, partial=True)
    product = stok.product
    date = datetime.date.today()
    quantity = int(request.data.get("quantity"))
    if quantity==0:
        return Response({"detail": "Say 0 ola bilməz"}, status=status.HTTP_400_BAD_REQUEST)
    executor = request.user
    evvelki_quantity = stok.quantity
    yekun_quantity = abs(int(evvelki_quantity) + int(quantity))
    
    if serializer.is_valid():
        note = serializer.validated_data.get("note")
        serializer.save(quantity=quantity)
        operation = Operation.objects.create(
                executor=executor,
                quantity=yekun_quantity,
                operation_type="stok yeniləmə",
                operation_date=date,
                note=note,
                shipping_warehouse=None,
                receiving_warehouse=None,
                product_and_quantity=product.product_name
            )
        operation.save()
        serializer.save(quantity=yekun_quantity)
        return Response({"detail": "Məlumatlar yeniləndi"}, status=status.HTTP_200_OK)
    else:
        return Response({"detail": "Xəta baş verdi!"}, status=status.HTTP_400_BAD_REQUEST)