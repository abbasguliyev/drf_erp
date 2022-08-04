from rest_framework import status, generics
from django_filters.rest_framework import DjangoFilterBackend

from restAPI.v1.cashbox.utils import (
    holding_umumi_balans_hesabla, 
    pul_axini_create, 
    ofis_balans_hesabla, 
    shirket_balans_hesabla, 
    holding_balans_hesabla
)
from rest_framework.response import Response

from restAPI.v1.cashbox.serializers import (
    PulAxiniSerializer,
    HoldingKassaSerializer,
    ShirketKassaSerializer,
    OfisKassaSerializer,
)

from cashbox.models import (
    HoldingKassa,
    ShirketKassa,
    OfisKassa,
    PulAxini
)

from restAPI.v1.cashbox.filters import (
    HoldingKassaFilter,
    OfisKassaFilter,
    PulAxiniFilter,
    ShirketKassaFilter,
)

from restAPI.v1.cashbox import permissions as company_permissions
from django.contrib.auth.models import Group
# ********************************** kassa put delete post get **********************************

class HoldingKassaListCreateAPIView(generics.ListCreateAPIView):
    queryset = HoldingKassa.objects.all()
    serializer_class = HoldingKassaSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = HoldingKassaFilter
    permission_classes = [company_permissions.HoldingKassaPermissions]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        user = request.user
        if serializer.is_valid():
            holding = serializer.validated_data.get("holding")
            balans = serializer.validated_data.get("balans")

            ilkin_balans = holding_umumi_balans_hesabla()
            print(f"{ilkin_balans=}")
            holding_ilkin_balans = holding_balans_hesabla()

            serializer.save()

            sonraki_balans = holding_umumi_balans_hesabla()
            print(f"{sonraki_balans=}")
            holding_sonraki_balans = holding_balans_hesabla()
            pul_axini_create(
                holding=holding,
                aciqlama=f"{holding.holding_adi} holdinq kassasına {float(balans)} AZN əlavə edildi",
                ilkin_balans=ilkin_balans,
                sonraki_balans=sonraki_balans,
                holding_ilkin_balans=holding_ilkin_balans,
                holding_sonraki_balans=holding_sonraki_balans,
                emeliyyat_eden=user,
                miqdar=float(balans)
            )
            return Response({"detail":"Holding kassa əlavə olundu"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"detail":"Məlumatları doğru daxil etdiyinizdən əmin olun"}, status=status.HTTP_400_BAD_REQUEST)



class HoldingKassaDetailAPIView(generics.RetrieveUpdateAPIView):
    queryset = HoldingKassa.objects.all()
    serializer_class = HoldingKassaSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = HoldingKassaFilter
    permission_classes = [company_permissions.HoldingKassaPermissions]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        user = request.user
        if serializer.is_valid():
            holding = instance.holding

            ilkin_balans = holding_umumi_balans_hesabla()
            print(f"{ilkin_balans=}")
            holding_ilkin_balans = holding_balans_hesabla()

            balans = serializer.validated_data.get("balans")

            serializer.save()

            sonraki_balans = holding_umumi_balans_hesabla()
            print(f"{sonraki_balans=}")
            holding_sonraki_balans = holding_balans_hesabla()
            pul_axini_create(
                holding=holding,
                aciqlama=f"{holding.holding_adi} holdinq kassasına {float(balans)} AZN əlavə edildi",
                ilkin_balans=ilkin_balans,
                sonraki_balans=sonraki_balans,
                holding_ilkin_balans=holding_ilkin_balans,
                holding_sonraki_balans=holding_sonraki_balans,
                emeliyyat_eden=user,
                miqdar=float(balans)
            )
            return Response({"detail":"Holding kassa məlumatları yeniləndi"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"detail":"Məlumatları doğru daxil etdiyinizdən əmin olun"}, status=status.HTTP_400_BAD_REQUEST)



# **********************************

class ShirketKassaListCreateAPIView(generics.ListCreateAPIView):
    queryset = ShirketKassa.objects.all()
    serializer_class = ShirketKassaSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ShirketKassaFilter
    permission_classes = [company_permissions.ShirketKassaPermissions]

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            queryset = ShirketKassa.objects.all()
        elif request.user.shirket is not None:
            queryset = ShirketKassa.objects.filter(shirket=request.user.shirket)
        else:
            queryset = ShirketKassa.objects.all()
        queryset = self.filter_queryset(queryset)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        user = request.user
        if serializer.is_valid():
            shirket = serializer.validated_data.get("shirket")
            balans = serializer.validated_data.get("balans")

            ilkin_balans = holding_umumi_balans_hesabla()
            print(f"{ilkin_balans=}")
            shirket_ilkin_balans = shirket_balans_hesabla(shirket=shirket)

            serializer.save()

            sonraki_balans = holding_umumi_balans_hesabla()
            print(f"{sonraki_balans=}")
            shirket_sonraki_balans = shirket_balans_hesabla(shirket=shirket)
            pul_axini_create(
                shirket=shirket,
                aciqlama=f"{shirket.shirket_adi} şirkət kassasına {float(balans)} AZN əlavə edildi",
                ilkin_balans=ilkin_balans,
                sonraki_balans=sonraki_balans,
                shirket_ilkin_balans=shirket_ilkin_balans,
                shirket_sonraki_balans=shirket_sonraki_balans,
                emeliyyat_eden=user,
                miqdar=float(balans)
            )
            return Response({"detail":"Şirkət kassa əlavə olundu"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"detail":"Məlumatları doğru daxil etdiyinizdən əmin olun"}, status=status.HTTP_400_BAD_REQUEST)



class ShirketKassaDetailAPIView(generics.RetrieveUpdateAPIView):
    queryset = ShirketKassa.objects.all()
    serializer_class = ShirketKassaSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ShirketKassaFilter
    permission_classes = [company_permissions.ShirketKassaPermissions]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        user = request.user
        if serializer.is_valid():
            shirket = instance.shirket

            balans = serializer.validated_data.get("balans")
            ilkin_balans = holding_umumi_balans_hesabla()
            print(f"{ilkin_balans=}")
            shirket_ilkin_balans = shirket_balans_hesabla(shirket=shirket)

            serializer.save()
            
            sonraki_balans = holding_umumi_balans_hesabla()
            print(f"{sonraki_balans=}")
            shirket_sonraki_balans = shirket_balans_hesabla(shirket=shirket)
            pul_axini_create(
                shirket=shirket,
                aciqlama=f"{shirket.shirket_adi} şirkət kassasına {float(balans)} AZN əlavə edildi",
                ilkin_balans=ilkin_balans,
                sonraki_balans=sonraki_balans,
                shirket_ilkin_balans=shirket_ilkin_balans,
                shirket_sonraki_balans=shirket_sonraki_balans,
                emeliyyat_eden=user,
                miqdar=float(balans)
            )
            return Response({"detail":"Şirkət kassa məlumatları yeniləndi"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"detail":"Məlumatları doğru daxil etdiyinizdən əmin olun"}, status=status.HTTP_400_BAD_REQUEST)



# **********************************

class OfisKassaListCreateAPIView(generics.ListCreateAPIView):
    queryset = OfisKassa.objects.all()
    serializer_class = OfisKassaSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = OfisKassaFilter
    permission_classes = [company_permissions.OfisKassaPermissions]

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            queryset = OfisKassa.objects.all()
        elif request.user.shirket is not None:
            if request.user.ofis is not None:
                queryset = OfisKassa.objects.filter(ofis__shirket=request.user.shirket, ofis=request.user.ofis)
            queryset = OfisKassa.objects.filter(ofis__shirket=request.user.shirket)
        else:
            queryset = OfisKassa.objects.all()
        queryset = self.filter_queryset(queryset)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        user = request.user
        if serializer.is_valid():
            ofis = serializer.validated_data.get("ofis")
            balans = serializer.validated_data.get("balans")

            ilkin_balans = holding_umumi_balans_hesabla()
            print(f"{ilkin_balans=}")
            ofis_ilkin_balans = ofis_balans_hesabla(ofis=ofis)

            serializer.save()

            sonraki_balans = holding_umumi_balans_hesabla()
            print(f"{sonraki_balans=}")
            ofis_sonraki_balans = ofis_balans_hesabla(ofis=ofis)
            pul_axini_create(
                ofis=ofis,
                shirket=ofis.shirket,
                aciqlama=f"{ofis.ofis_adi} ofis kassasına {float(balans)} AZN əlavə edildi",
                ilkin_balans=ilkin_balans,
                sonraki_balans=sonraki_balans,
                ofis_ilkin_balans=ofis_ilkin_balans,
                ofis_sonraki_balans=ofis_sonraki_balans,
                emeliyyat_eden=user,
                miqdar=float(balans)
            )
            return Response({"detail":"Ofis kassa əlavə olundu"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"detail":"Məlumatları doğru daxil etdiyinizdən əmin olun"}, status=status.HTTP_400_BAD_REQUEST)



class OfisKassaDetailAPIView(generics.RetrieveUpdateAPIView):
    queryset = OfisKassa.objects.all()
    serializer_class = OfisKassaSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = OfisKassaFilter
    permission_classes = [company_permissions.OfisKassaPermissions]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        user = request.user
        if serializer.is_valid():
            ofis = instance.ofis
            balans = serializer.validated_data.get("balans")
            
            ilkin_balans = holding_umumi_balans_hesabla()
            print(f"{ilkin_balans=}")
            ofis_ilkin_balans = ofis_balans_hesabla(ofis=ofis)

            serializer.save()
            
            sonraki_balans = holding_umumi_balans_hesabla()
            print(f"{sonraki_balans=}")
            ofis_sonraki_balans = ofis_balans_hesabla(ofis=ofis)
            pul_axini_create(
                ofis=ofis,
                shirket=ofis.shirket,
                aciqlama=f"{ofis.ofis_adi} ofis kassasına {float(balans)} AZN əlavə edildi",
                ilkin_balans=ilkin_balans,
                sonraki_balans=sonraki_balans,
                ofis_ilkin_balans=ofis_ilkin_balans,
                ofis_sonraki_balans=ofis_sonraki_balans,
                emeliyyat_eden=user,
                miqdar=float(balans)
            )
            return Response({"detail":"Ofis kassa məlumatları yeniləndi"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"detail":"Məlumatları doğru daxil etdiyinizdən əmin olun"}, status=status.HTTP_400_BAD_REQUEST)

# ********************************** Pul Axini get **********************************

class PulAxiniListAPIView(generics.ListAPIView):
    queryset = PulAxini.objects.all()
    serializer_class = PulAxiniSerializer
    permission_classes = [company_permissions.PulAxiniPermissions]
    filter_backends = [DjangoFilterBackend]
    filterset_class = PulAxiniFilter

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        
        # umumi_miqdar = queryset.count()
        umumi_miqdar = 0

        for q in queryset:
            umumi_miqdar += q.miqdar

        print(f"{umumi_miqdar=}")

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response([
                {'umumi_miqdar': umumi_miqdar, 'data':serializer.data}
            ])

        serializer = self.get_serializer(queryset, many=True)
        return Response([
                {'umumi_miqdar': umumi_miqdar, 'data':serializer.data}
            ])

class PulAxiniDetailAPIView(generics.RetrieveAPIView):
    queryset = PulAxini.objects.all()
    serializer_class = PulAxiniSerializer
    permission_classes = [company_permissions.PulAxiniPermissions]
    filter_backends = [DjangoFilterBackend]
    filterset_class = PulAxiniFilter