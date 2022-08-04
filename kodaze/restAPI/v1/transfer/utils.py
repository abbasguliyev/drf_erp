from rest_framework import status
from rest_framework.response import Response

def holding_shirket_transfer_create(self, request, *args, **kwargs):
    """
        Holdingden sirketlere transfer ucun istifade olunan method
    """
    serializer = self.get_serializer(data=request.data)
    user = request.user

    if (serializer.is_valid()):
        transfer_meblegi = serializer.validated_data.get("transfer_meblegi")
        gonderen_kassa = serializer.validated_data.get("holding_kassa")
        gonderen_kassa_balans = gonderen_kassa.balans
        gonderilen_kassalar = serializer.validated_data.get("shirket_kassa")
        gonderilen_kassalar_cemi = len(gonderilen_kassalar)
        evvelki_balans = gonderen_kassa_balans

        if(len(gonderilen_kassalar) == 0):
            return Response({"detail": "Heç bir ofis daxil etməmisiniz"}, status=status.HTTP_400_BAD_REQUEST)

        if (transfer_meblegi != None):
            if float(transfer_meblegi) <= float(gonderen_kassa_balans):
                gonderen_kassa_yekun_balans = float(
                    gonderen_kassa_balans) - (float(transfer_meblegi) * gonderilen_kassalar_cemi)
                gonderen_kassa.balans = gonderen_kassa_yekun_balans
                sonraki_balans = gonderen_kassa_yekun_balans
                gonderen_kassa.save()
                # qalan_mebleg = float(gonderen_kassa_balans) - float(transfer_meblegi)
            else:
                return Response({"detail": "Transfer məbləği kassanın balansıdan böyük ola bilməz"},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"detail": "Məbləği doğru daxil edin"}, status=status.HTTP_400_BAD_REQUEST)

        for i in gonderilen_kassalar:
            gonderilen_kassa = i
            gonderilen_kassa_balans = gonderilen_kassa.balans
            gonderilen_kassa_balans = float(
                transfer_meblegi) + float(gonderilen_kassa_balans)

            gonderilen_kassa.balans = gonderilen_kassa_balans
            gonderilen_kassa.save()

        serializer.save(qalan_mebleg=gonderen_kassa.balans, evvelki_balans=evvelki_balans,
                        sonraki_balans=sonraki_balans, transfer_eden=user)
        return Response({"detail": "Transfer edildi"}, status=status.HTTP_201_CREATED)
    else:
        return Response({"detail": "Məlumatları doğru daxil edin"}, status=status.HTTP_400_BAD_REQUEST)


def shirket_holding_transfer_create(self, request, *args, **kwargs):
    """
        Sirketden holdinge transfer ucun istifade olunan method
    """
    serializer = self.get_serializer(data=request.data)
    user = request.user

    if (serializer.is_valid()):
        gonderen_kassa = serializer.validated_data.get("shirket_kassa")
        transfer_meblegi = request.data.get("transfer_meblegi")

        gonderen_kassa_balans = gonderen_kassa.balans
        evvelki_balans = gonderen_kassa_balans
        # qalan_mebleg = float(gonderen_kassa_balans) - float(transfer_meblegi)

        if (transfer_meblegi != None):
            if float(transfer_meblegi) <= float(gonderen_kassa_balans):
                gonderen_kassa.balans = float(
                    gonderen_kassa_balans) - float(transfer_meblegi)
                gonderen_kassa.save()
                sonraki_balans = gonderen_kassa.balans
            else:
                return Response({"detail": "Transfer məbləği kassanın balansıdan böyük ola bilməz"},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"detail": "Məbləği doğru daxil edin"}, status=status.HTTP_400_BAD_REQUEST)

        gonderilen_kassa = serializer.validated_data.get("holding_kassa")

        gonderilen_kassa_balans = gonderilen_kassa.balans
        gonderilen_kassa.balans = float(
            transfer_meblegi) + float(gonderilen_kassa_balans)
        gonderilen_kassa.save()

        serializer.save(qalan_mebleg=gonderen_kassa.balans, evvelki_balans=evvelki_balans,
                        sonraki_balans=sonraki_balans, transfer_eden=user)

        return Response({"detail": "Transfer edildi"}, status=status.HTTP_201_CREATED)
    else:
        return Response({"detail": "Məlumatları doğru daxil edin"}, status=status.HTTP_400_BAD_REQUEST)


def shirket_ofis_transfer_create(self, request, *args, **kwargs):
    """
        Sirketden ofislere transfer ucun istifade olunan method
    """
    serializer = self.get_serializer(data=request.data)
    user = request.user

    if (serializer.is_valid()):
        transfer_meblegi = serializer.validated_data.get("transfer_meblegi")
        gonderen_kassa = serializer.validated_data.get("shirket_kassa")
        gonderen_kassa_balans = gonderen_kassa.balans
        gonderilen_kassalar = serializer.validated_data.get("ofis_kassa")
        if(len(gonderilen_kassalar) == 0):
            return Response({"detail": "Heç bir ofis daxil etməmisiniz"}, status=status.HTTP_400_BAD_REQUEST)

        gonderilen_kassalar_cemi = len(gonderilen_kassalar)
        evvelki_balans = gonderen_kassa_balans

        if (transfer_meblegi != None):
            if float(transfer_meblegi) <= float(gonderen_kassa_balans):
                gonderen_kassa_yekun_balans = float(gonderen_kassa_balans) - (
                    float(transfer_meblegi) * gonderilen_kassalar_cemi)
                gonderen_kassa.balans = gonderen_kassa_yekun_balans
                sonraki_balans = gonderen_kassa_yekun_balans
                gonderen_kassa.save()
                # qalan_mebleg = float(gonderen_kassa_balans) - float(transfer_meblegi)
            else:
                return Response({"detail": "Transfer məbləği kassanın balansıdan böyük ola bilməz"},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"detail": "Məbləği doğru daxil edin"}, status=status.HTTP_400_BAD_REQUEST)

        for i in gonderilen_kassalar:
            gonderilen_kassa = i
            gonderilen_kassa_balans = gonderilen_kassa.balans
            gonderilen_kassa_balans = float(
                transfer_meblegi) + float(gonderilen_kassa_balans)

            gonderilen_kassa.balans = gonderilen_kassa_balans
            gonderilen_kassa.save()

        serializer.save(qalan_mebleg=gonderen_kassa.balans, evvelki_balans=evvelki_balans,
                        sonraki_balans=sonraki_balans, transfer_eden=user)
        return Response({"detail": "Transfer edildi"}, status=status.HTTP_201_CREATED)
    else:
        return Response({"detail": "Məlumatları doğru daxil edin"}, status=status.HTTP_400_BAD_REQUEST)


def ofis_shirket_transfer_create(self, request, *args, **kwargs):
    """
        Ofisden sirkete transfer ucun istifade olunan method
    """
    serializer = self.get_serializer(data=request.data)
    user = request.user

    if (serializer.is_valid()):
        gonderen_kassa = serializer.validated_data.get("ofis_kassa")
        transfer_meblegi = request.data.get("transfer_meblegi")

        gonderen_kassa_balans = gonderen_kassa.balans
        evvelki_balans = gonderen_kassa_balans
        # qalan_mebleg = float(gonderen_kassa_balans) - float(transfer_meblegi)

        if (transfer_meblegi != None):
            if float(transfer_meblegi) <= float(gonderen_kassa_balans):
                gonderen_kassa.balans = float(
                    gonderen_kassa_balans) - float(transfer_meblegi)
                sonraki_balans = gonderen_kassa.balans
                gonderen_kassa.save()
            else:
                return Response({"detail": "Transfer məbləği kassanın balansıdan böyük ola bilməz"},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"detail": "Məbləği doğru daxil edin"}, status=status.HTTP_400_BAD_REQUEST)

        gonderilen_kassa = serializer.validated_data.get("shirket_kassa")

        gonderilen_kassa_balans = gonderilen_kassa.balans

        gonderilen_kassa.balans = float(
            transfer_meblegi) + float(gonderilen_kassa_balans)
        gonderilen_kassa.save()

        serializer.save(qalan_mebleg=gonderen_kassa.balans, evvelki_balans=evvelki_balans,
                        sonraki_balans=sonraki_balans, transfer_eden=user)

        return Response({"detail": "Transfer edildi"}, status=status.HTTP_201_CREATED)
    else:
        return Response({"detail": "Məlumatları doğru daxil edin"}, status=status.HTTP_400_BAD_REQUEST)
