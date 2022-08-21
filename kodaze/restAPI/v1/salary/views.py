from salary.models import (
    Avans,
    DealerPrimNew,
    Kesinti,
    Bonus,
    KreditorPrim,
    MaasGoruntuleme,
    MaasOde, 
    VanLeaderPrim, 
    DealerPrim, 
    OfficeLeaderPrim,
    CanvasserPrim,
    VanLeaderPrimNew
)
from restAPI.v1.salary.serializers import (
    AvansSerializer, 
    BonusSerializer,
    DealerPrimNewSerializer,
    KesintiSerializer,
    MaasGoruntulemeSerializer,
    CanvasserPrimSerializer,
    DealerPrimSerializer,
    MaasOdeSerializer,
    OfficeLeaderPrimSerializer,
    VanLeaderPrimNewSerializer,
    VanLeaderPrimSerializer,
    KreditorPrimSerializer,
)
from rest_framework import status, generics

from rest_framework.response import Response

from restAPI.v1.salary import utils as salary_utils

from restAPI.v1.salary import permissions as maas_permissions

from django_filters.rest_framework import DjangoFilterBackend

from restAPI.v1.salary.filters import (
    AvansFilter,
    BonusFilter,
    CanvasserPrimFilter,
    DealerPrimFilter,
    DealerPrimNewFilter,
    KesintiFilter,
    MaasGoruntulemeFilter,
    MaasOdeFilter,
    OfficeLeaderPrimFilter,
    VanLeaderPrimFilter,
    VanLeaderPrimNewFilter
)

# ********************************** Avans get post put delete **********************************
class AvansListCreateAPIView(generics.ListCreateAPIView):
    queryset = Avans.objects.all()
    serializer_class = AvansSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = AvansFilter
    permission_classes = [maas_permissions.AvansPermissions]

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            queryset = Avans.objects.all()
        elif request.user.shirket is not None:
            if request.user.ofis is not None:
                queryset = Avans.objects.filter(isci__shirket=request.user.shirket, isci__ofis=request.user.ofis)
            queryset = Avans.objects.filter(isci__shirket=request.user.shirket)
        else:
            queryset = Avans.objects.all()
        queryset = self.filter_queryset(queryset)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        return salary_utils.avans_create(self, request, *args, **kwargs)

class AvansDetailAPIView(generics.RetrieveUpdateAPIView):
    queryset = Avans.objects.all()
    serializer_class = AvansSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = AvansFilter
    permission_classes = [maas_permissions.AvansPermissions]

# ********************************** Kesinti get post put delete **********************************
class KesintiListCreateAPIView(generics.ListCreateAPIView):
    queryset = Kesinti.objects.all()
    serializer_class = KesintiSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = KesintiFilter
    permission_classes = [maas_permissions.KesintiPermissions]

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            queryset = Kesinti.objects.all()
        elif request.user.shirket is not None:
            if request.user.ofis is not None:
                queryset = Kesinti.objects.filter(isci__shirket=request.user.shirket, isci__ofis=request.user.ofis)
            queryset = Kesinti.objects.filter(isci__shirket=request.user.shirket)
        else:
            queryset = Kesinti.objects.all()
        queryset = self.filter_queryset(queryset)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        return salary_utils.kesinti_create(self, request, *args, **kwargs)


class KesintiDetailAPIView(generics.RetrieveUpdateAPIView):
    queryset = Kesinti.objects.all()
    serializer_class = KesintiSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = KesintiFilter
    permission_classes = [maas_permissions.KesintiPermissions]

# ********************************** Bonus get post put delete **********************************
class BonusListCreateAPIView(generics.ListCreateAPIView):
    queryset = Bonus.objects.all()
    serializer_class = BonusSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = BonusFilter
    permission_classes = [maas_permissions.BonusPermissions]

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            queryset = Bonus.objects.all()
        elif request.user.shirket is not None:
            if request.user.ofis is not None:
                queryset = Bonus.objects.filter(isci__shirket=request.user.shirket, isci__ofis=request.user.ofis)
            queryset = Bonus.objects.filter(isci__shirket=request.user.shirket)
        else:
            queryset = Bonus.objects.all()
        queryset = self.filter_queryset(queryset)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        return salary_utils.bonus_create(self, request, *args, **kwargs)


class BonusDetailAPIView(generics.RetrieveUpdateAPIView):
    queryset = Bonus.objects.all()
    serializer_class = BonusSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = BonusFilter
    permission_classes = [maas_permissions.BonusPermissions]

# ********************************** Maas Ode get post put delete **********************************
class MaasOdeListCreateAPIView(generics.ListCreateAPIView):
    queryset = MaasOde.objects.all()
    serializer_class = MaasOdeSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = MaasOdeFilter
    permission_classes = [maas_permissions.MaasOdePermissions]

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            queryset = MaasOde.objects.all()
        elif request.user.shirket is not None:
            if request.user.ofis is not None:
                queryset = MaasOde.objects.filter(isci__shirket=request.user.shirket, isci__ofis=request.user.ofis)
            queryset = MaasOde.objects.filter(isci__shirket=request.user.shirket)
        else:
            queryset = MaasOde.objects.all()
        queryset = self.filter_queryset(queryset)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        return salary_utils.maas_ode_create(self, request, *args, **kwargs)


class MaasOdeDetailAPIView(generics.RetrieveUpdateAPIView):
    queryset = MaasOde.objects.all()
    serializer_class = MaasOdeSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = MaasOdeFilter
    permission_classes = [maas_permissions.MaasOdePermissions]

# ********************************** MaasGoruntuleme get post put delete **********************************
class MaasGoruntulemeListCreateAPIView(generics.ListCreateAPIView):
    queryset = MaasGoruntuleme.objects.all()
    serializer_class = MaasGoruntulemeSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = MaasGoruntulemeFilter
    permission_classes = [maas_permissions.MaasGoruntulemePermissions]

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            queryset = MaasGoruntuleme.objects.all()
        elif request.user.shirket is not None:
            if request.user.ofis is not None:
                queryset = MaasGoruntuleme.objects.filter(isci__shirket=request.user.shirket, isci__ofis=request.user.ofis)
            queryset = MaasGoruntuleme.objects.filter(isci__shirket=request.user.shirket)
        else:
            queryset = MaasGoruntuleme.objects.all()
        queryset = self.filter_queryset(queryset)
    
        satis_sayi = 0
        umumi_avans = 0
        umumi_bonus = 0
        umumi_kesinti = 0

        for q in queryset:
            satis_sayi += q.satis_sayi

            month = q.tarix.month

            avans = Avans.objects.filter(isci = q.isci, avans_tarixi__month=month)
            bonus = Bonus.objects.filter(isci = q.isci, bonus_tarixi__month=month)
            kesinti = Kesinti.objects.filter(isci = q.isci, kesinti_tarixi__month=month)

            for a in avans:
                umumi_avans += a.mebleg

            for b in bonus:
                umumi_bonus += b.mebleg

            for k in kesinti:
                umumi_kesinti += k.mebleg

        print(f"{umumi_avans=}")
        print(f"{umumi_bonus=}")
        print(f"{umumi_kesinti=}")

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(
                {
                    'umumi_avans': umumi_avans, 
                    'umumi_bonus': umumi_bonus, 
                    'umumi_kesinti': umumi_kesinti,
                    'data':serializer.data
                }
            )

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class MaasGoruntulemeDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MaasGoruntuleme.objects.all()
    serializer_class = MaasGoruntulemeSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = MaasGoruntulemeFilter
    permission_classes = [maas_permissions.MaasGoruntulemePermissions]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"detail": "Əməliyyat yerinə yetirildi"}, status=status.HTTP_204_NO_CONTENT)

# ********************************** Office Leader Prim get post put delete **********************************
class OfficeLeaderPrimListCreateAPIView(generics.ListCreateAPIView):
    queryset = OfficeLeaderPrim.objects.all()
    serializer_class = OfficeLeaderPrimSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = OfficeLeaderPrimFilter
    permission_classes = [maas_permissions.OfficeLeaderPrimPermissions]

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            queryset = OfficeLeaderPrim.objects.all()
        elif request.user.shirket is not None:
            queryset = OfficeLeaderPrim.objects.filter(vezife__shirket=request.user.shirket)
        else:
            queryset = OfficeLeaderPrim.objects.all()
        queryset = self.filter_queryset(queryset)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            prim_status = serializer.validated_data.get("prim_status")
            vezife = serializer.validated_data.get("vezife")
            prim = OfficeLeaderPrim.objects.filter(prim_status=prim_status, vezife=vezife)
            print(f"{prim=}")
            if len(prim)>0:
                return Response({"detail": "Bu status və vəzifəyə uyğun prim artıq əlavə olunub"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                serializer.save()
                return Response({"detail": "Prim əlavə edildi"})


class OfficeLeaderPrimDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = OfficeLeaderPrim.objects.all()
    serializer_class = OfficeLeaderPrimSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = OfficeLeaderPrimFilter
    permission_classes = [maas_permissions.OfficeLeaderPrimPermissions]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "Office Leader bonus yeniləndi"}, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"detail": "Əməliyyat yerinə yetirildi"}, status=status.HTTP_204_NO_CONTENT)
# ********************************** VanLeader Prim get post put delete **********************************
class VanLeaderPrimListCreateAPIView(generics.ListCreateAPIView):
    queryset = VanLeaderPrim.objects.all()
    serializer_class = VanLeaderPrimSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = VanLeaderPrimFilter
    permission_classes = [maas_permissions.VanLeaderPrimPermissions]

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            queryset = VanLeaderPrim.objects.all()
        elif request.user.shirket is not None:
            queryset = VanLeaderPrim.objects.filter(vezife__shirket=request.user.shirket)
        else:
            queryset = VanLeaderPrim.objects.all()
        queryset = self.filter_queryset(queryset)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # mehsul = serializer.validated_data.get("mehsul")
            # satis_meblegi = serializer.validated_data.get("satis_meblegi")
            # if (satis_meblegi == None) or (satis_meblegi == ""):
            #     satis_meblegi = mehsul.qiymet
            
            serializer.save()

            return Response({"detail": "Prim əlavə edildi"})


class VanLeaderPrimDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = VanLeaderPrim.objects.all()
    serializer_class = VanLeaderPrimSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = VanLeaderPrimFilter
    permission_classes = [maas_permissions.VanLeaderPrimPermissions]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "Van Leader bonus yeniləndi"}, status=status.HTTP_200_OK)

# ********************************** VanLeader Prim New get post put delete **********************************
class VanLeaderPrimNewListCreateAPIView(generics.ListCreateAPIView):
    queryset = VanLeaderPrimNew.objects.all()
    serializer_class = VanLeaderPrimNewSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = VanLeaderPrimNewFilter
    permission_classes = [maas_permissions.VanLeaderPrimNewPermissions]

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            queryset = VanLeaderPrimNew.objects.all()
        elif request.user.shirket is not None:
            queryset = VanLeaderPrimNew.objects.filter(vezife__shirket=request.user.shirket)
        else:
            queryset = VanLeaderPrimNew.objects.all()
        queryset = self.filter_queryset(queryset)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            prim_status = serializer.validated_data.get("prim_status")
            vezife = serializer.validated_data.get("vezife")
            prim = VanLeaderPrimNew.objects.filter(prim_status=prim_status, vezife=vezife)
            print(f"{prim=}")
            if len(prim)>0:
                return Response({"detail": "Bu status və vəzifəyə uyğun prim artıq əlavə olunub"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                serializer.save()
                return Response({"detail": "Prim əlavə edildi"})


class VanLeaderPrimNewDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = VanLeaderPrimNew.objects.all()
    serializer_class = VanLeaderPrimNewSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = VanLeaderPrimNewFilter
    permission_classes = [maas_permissions.VanLeaderPrimNewPermissions]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "Van Leader bonus yeniləndi"}, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"detail": "Əməliyyat yerinə yetirildi"}, status=status.HTTP_204_NO_CONTENT)

# ********************************** Canvasser Prim get post put delete **********************************
class CanvasserPrimListCreateAPIView(generics.ListCreateAPIView):
    queryset = CanvasserPrim.objects.all()
    serializer_class = CanvasserPrimSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CanvasserPrimFilter
    permission_classes = [maas_permissions.CanvasserPrimPermissions]

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            queryset = CanvasserPrim.objects.all()
        elif request.user.shirket is not None:
            queryset = CanvasserPrim.objects.filter(vezife__shirket=request.user.shirket)
        else:
            queryset = CanvasserPrim.objects.all()
        queryset = self.filter_queryset(queryset)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            prim_status = serializer.validated_data.get("prim_status")
            vezife = serializer.validated_data.get("vezife")
            prim = CanvasserPrim.objects.filter(prim_status=prim_status, vezife=vezife)
            print(f"{prim=}")
            if len(prim)>0:
                return Response({"detail": "Bu status və vəzifəyə uyğun prim artıq əlavə olunub"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                serializer.save()
                return Response({"detail": "Prim əlavə edildi"})

class CanvasserPrimDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CanvasserPrim.objects.all()
    serializer_class = CanvasserPrimSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CanvasserPrimFilter
    permission_classes = [maas_permissions.CanvasserPrimPermissions]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "Canvasser bonus yeniləndi"}, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"detail": "Əməliyyat yerinə yetirildi"}, status=status.HTTP_204_NO_CONTENT)

# ********************************** Dealer Prim get post put delete **********************************
class DealerPrimListCreateAPIView(generics.ListCreateAPIView):
    queryset = DealerPrim.objects.all()
    serializer_class = DealerPrimSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = DealerPrimFilter
    permission_classes = [maas_permissions.DealerPrimPermissions]

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            queryset = DealerPrim.objects.all()
        elif request.user.shirket is not None:
            queryset = DealerPrim.objects.filter(vezife__shirket=request.user.shirket)
        else:
            queryset = DealerPrim.objects.all()
        queryset = self.filter_queryset(queryset)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # mehsul = serializer.validated_data.get("mehsul")
            # satis_meblegi = serializer.validated_data.get("satis_meblegi")
            # if (satis_meblegi == None) or (satis_meblegi == ""):
            #     satis_meblegi = mehsul.qiymet
            
            serializer.save()

            return Response({"detail": "Prim əlavə edildi"})

class DealerPrimDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = DealerPrim.objects.all()
    serializer_class = DealerPrimSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = DealerPrimFilter
    permission_classes = [maas_permissions.DealerPrimPermissions]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "Dealer bonus yeniləndi"}, status=status.HTTP_200_OK)
    
# ********************************** Dealer Prim New get post put delete **********************************
class DealerPrimNewListCreateAPIView(generics.ListCreateAPIView):
    queryset = DealerPrimNew.objects.all()
    serializer_class = DealerPrimNewSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = DealerPrimNewFilter
    permission_classes = [maas_permissions.DealerPrimNewPermissions]

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            queryset = DealerPrimNew.objects.all()
        elif request.user.shirket is not None:
            queryset = DealerPrimNew.objects.filter(vezife__shirket=request.user.shirket)
        else:
            queryset = DealerPrimNew.objects.all()
        queryset = self.filter_queryset(queryset)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            prim_status = serializer.validated_data.get("prim_status")
            vezife = serializer.validated_data.get("vezife")
            prim = DealerPrimNew.objects.filter(prim_status=prim_status, vezife=vezife)
            print(f"{prim=}")
            if len(prim)>0:
                return Response({"detail": "Bu status və vəzifəyə uyğun prim artıq əlavə olunub"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                serializer.save()
                return Response({"detail": "Prim əlavə edildi"})

class DealerPrimNewDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = DealerPrimNew.objects.all()
    serializer_class = DealerPrimNewSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = DealerPrimNewFilter
    permission_classes = [maas_permissions.DealerPrimNewPermissions]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "Dealer bonus yeniləndi"}, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"detail": "Əməliyyat yerinə yetirildi"}, status=status.HTTP_204_NO_CONTENT)

# ********************************** Kreditor Prim get post put delete **********************************
class KreditorPrimListCreateAPIView(generics.ListCreateAPIView):
    queryset = KreditorPrim.objects.all()
    serializer_class = KreditorPrimSerializer
    permission_classes = [maas_permissions.KreditorPrimPermissions]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({"detail": "Kreditor prim əlavə olundu"}, status=status.HTTP_201_CREATED, headers=headers)

class KreditorPrimDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = KreditorPrim.objects.all()
    serializer_class = KreditorPrimSerializer
    permission_classes = [maas_permissions.KreditorPrimPermissions]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "Kredit bonus faizi yeniləndi"}, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"detail": "Əməliyyat yerinə yetirildi"}, status=status.HTTP_204_NO_CONTENT)