from rest_framework import status
from rest_framework.response import Response

def holding_company_transfer_create(self, request, *args, **kwargs):
    """
        Holdingden sirketlere transfer ucun istifade olunan method
    """
    serializer = self.get_serializer(data=request.data)
    user = request.user

    if (serializer.is_valid()):
        transfer_amount = serializer.validated_data.get("transfer_amount")
        shipping_warehouse_kassa = serializer.validated_data.get("cashbox")
        shipping_warehouse_kassa_balance = shipping_warehouse_kassa.balance
        gonderilen_kassalar = serializer.validated_data.get("cashbox")
        gonderilen_kassalar_cemi = len(gonderilen_kassalar)
        previous_balance = shipping_warehouse_kassa_balance

        if(len(gonderilen_kassalar) == 0):
            return Response({"detail": "Heç bir office daxil etməmisiniz"}, status=status.HTTP_400_BAD_REQUEST)

        if (transfer_amount != None):
            if float(transfer_amount) <= float(shipping_warehouse_kassa_balance):
                shipping_warehouse_kassa_yekun_balance = float(
                    shipping_warehouse_kassa_balance) - (float(transfer_amount) * gonderilen_kassalar_cemi)
                shipping_warehouse_kassa.balance = shipping_warehouse_kassa_yekun_balance
                subsequent_balance = shipping_warehouse_kassa_yekun_balance
                shipping_warehouse_kassa.save()
                # qalan_amount = float(shipping_warehouse_kassa_balance) - float(transfer_amount)
            else:
                return Response({"detail": "Transfer məbləği kassanın balansıdan böyük ola bilməz"},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"detail": "Məbləği doğru daxil edin"}, status=status.HTTP_400_BAD_REQUEST)

        for i in gonderilen_kassalar:
            gonderilen_kassa = i
            gonderilen_kassa_balance = gonderilen_kassa.balance
            gonderilen_kassa_balance = float(
                transfer_amount) + float(gonderilen_kassa_balance)

            gonderilen_kassa.balance = gonderilen_kassa_balance
            gonderilen_kassa.save()

        serializer.save(qalan_amount=shipping_warehouse_kassa.balance, previous_balance=previous_balance,
                        subsequent_balance=subsequent_balance, executor=user)
        return Response({"detail": "Transfer edildi"}, status=status.HTTP_201_CREATED)
    else:
        return Response({"detail": "Məlumatları doğru daxil edin"}, status=status.HTTP_400_BAD_REQUEST)


def company_holding_transfer_create(self, request, *args, **kwargs):
    """
        Sirketden holdinge transfer ucun istifade olunan method
    """
    serializer = self.get_serializer(data=request.data)
    user = request.user

    if (serializer.is_valid()):
        shipping_warehouse_kassa = serializer.validated_data.get("cashbox")
        transfer_amount = request.data.get("transfer_amount")

        shipping_warehouse_kassa_balance = shipping_warehouse_kassa.balance
        previous_balance = shipping_warehouse_kassa_balance
        # qalan_amount = float(shipping_warehouse_kassa_balance) - float(transfer_amount)

        if (transfer_amount != None):
            if float(transfer_amount) <= float(shipping_warehouse_kassa_balance):
                shipping_warehouse_kassa.balance = float(
                    shipping_warehouse_kassa_balance) - float(transfer_amount)
                shipping_warehouse_kassa.save()
                subsequent_balance = shipping_warehouse_kassa.balance
            else:
                return Response({"detail": "Transfer məbləği kassanın balansıdan böyük ola bilməz"},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"detail": "Məbləği doğru daxil edin"}, status=status.HTTP_400_BAD_REQUEST)

        gonderilen_kassa = serializer.validated_data.get("cashbox")

        gonderilen_kassa_balance = gonderilen_kassa.balance
        gonderilen_kassa.balance = float(
            transfer_amount) + float(gonderilen_kassa_balance)
        gonderilen_kassa.save()

        serializer.save(qalan_amount=shipping_warehouse_kassa.balance, previous_balance=previous_balance,
                        subsequent_balance=subsequent_balance, executor=user)

        return Response({"detail": "Transfer edildi"}, status=status.HTTP_201_CREATED)
    else:
        return Response({"detail": "Məlumatları doğru daxil edin"}, status=status.HTTP_400_BAD_REQUEST)


def offices_transfer_create(self, request, *args, **kwargs):
    """
        Sirketden officelere transfer ucun istifade olunan method
    """
    serializer = self.get_serializer(data=request.data)
    user = request.user

    if (serializer.is_valid()):
        transfer_amount = serializer.validated_data.get("transfer_amount")
        shipping_warehouse_kassa = serializer.validated_data.get("cashbox")
        shipping_warehouse_kassa_balance = shipping_warehouse_kassa.balance
        gonderilen_kassalar = serializer.validated_data.get("cashbox")
        if(len(gonderilen_kassalar) == 0):
            return Response({"detail": "Heç bir office daxil etməmisiniz"}, status=status.HTTP_400_BAD_REQUEST)

        gonderilen_kassalar_cemi = len(gonderilen_kassalar)
        previous_balance = shipping_warehouse_kassa_balance

        if (transfer_amount != None):
            if float(transfer_amount) <= float(shipping_warehouse_kassa_balance):
                shipping_warehouse_kassa_yekun_balance = float(shipping_warehouse_kassa_balance) - (
                    float(transfer_amount) * gonderilen_kassalar_cemi)
                shipping_warehouse_kassa.balance = shipping_warehouse_kassa_yekun_balance
                subsequent_balance = shipping_warehouse_kassa_yekun_balance
                shipping_warehouse_kassa.save()
                # qalan_amount = float(shipping_warehouse_kassa_balance) - float(transfer_amount)
            else:
                return Response({"detail": "Transfer məbləği kassanın balansıdan böyük ola bilməz"},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"detail": "Məbləği doğru daxil edin"}, status=status.HTTP_400_BAD_REQUEST)

        for i in gonderilen_kassalar:
            gonderilen_kassa = i
            gonderilen_kassa_balance = gonderilen_kassa.balance
            gonderilen_kassa_balance = float(
                transfer_amount) + float(gonderilen_kassa_balance)

            gonderilen_kassa.balance = gonderilen_kassa_balance
            gonderilen_kassa.save()

        serializer.save(qalan_amount=shipping_warehouse_kassa.balance, previous_balance=previous_balance,
                        subsequent_balance=subsequent_balance, executor=user)
        return Response({"detail": "Transfer edildi"}, status=status.HTTP_201_CREATED)
    else:
        return Response({"detail": "Məlumatları doğru daxil edin"}, status=status.HTTP_400_BAD_REQUEST)


def office_company_transfer_create(self, request, *args, **kwargs):
    """
        Officeden sirkete transfer ucun istifade olunan method
    """
    serializer = self.get_serializer(data=request.data)
    user = request.user

    if (serializer.is_valid()):
        shipping_warehouse_kassa = serializer.validated_data.get("cashbox")
        transfer_amount = request.data.get("transfer_amount")

        shipping_warehouse_kassa_balance = shipping_warehouse_kassa.balance
        previous_balance = shipping_warehouse_kassa_balance
        # qalan_amount = float(shipping_warehouse_kassa_balance) - float(transfer_amount)

        if (transfer_amount != None):
            if float(transfer_amount) <= float(shipping_warehouse_kassa_balance):
                shipping_warehouse_kassa.balance = float(
                    shipping_warehouse_kassa_balance) - float(transfer_amount)
                subsequent_balance = shipping_warehouse_kassa.balance
                shipping_warehouse_kassa.save()
            else:
                return Response({"detail": "Transfer məbləği kassanın balansıdan böyük ola bilməz"},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"detail": "Məbləği doğru daxil edin"}, status=status.HTTP_400_BAD_REQUEST)

        gonderilen_kassa = serializer.validated_data.get("cashbox")

        gonderilen_kassa_balance = gonderilen_kassa.balance

        gonderilen_kassa.balance = float(
            transfer_amount) + float(gonderilen_kassa_balance)
        gonderilen_kassa.save()

        serializer.save(qalan_amount=shipping_warehouse_kassa.balance, previous_balance=previous_balance,
                        subsequent_balance=subsequent_balance, executor=user)

        return Response({"detail": "Transfer edildi"}, status=status.HTTP_201_CREATED)
    else:
        return Response({"detail": "Məlumatları doğru daxil edin"}, status=status.HTTP_400_BAD_REQUEST)
