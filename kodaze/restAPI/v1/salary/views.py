from salary.models import (
    Avans,
    Menecer1PrimNew,
    Kesinti,
    Bonus,
    KreditorPrim,
    MaasGoruntuleme,
    MaasOde, 
    GroupLeaderPrim, 
    Menecer1Prim, 
    OfficeLeaderPrim,
    Menecer2Prim,
    GroupLeaderPrimNew
)
from restAPI.v1.salary.serializers import (
    AvansSerializer, 
    BonusSerializer,
    Menecer1PrimNewSerializer,
    KesintiSerializer,
    MaasGoruntulemeSerializer,
    Menecer2PrimSerializer,
    Menecer1PrimSerializer,
    MaasOdeSerializer,
    OfficeLeaderPrimSerializer,
    GroupLeaderPrimNewSerializer,
    GroupLeaderPrimSerializer,
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
    Menecer2PrimFilter,
    Menecer1PrimFilter,
    Menecer1PrimNewFilter,
    KesintiFilter,
    MaasGoruntulemeFilter,
    MaasOdeFilter,
    OfficeLeaderPrimFilter,
    GroupLeaderPrimFilter,
    GroupLeaderPrimNewFilter
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
# ********************************** GroupLeader Prim get post put delete **********************************
class GroupLeaderPrimListCreateAPIView(generics.ListCreateAPIView):
    queryset = GroupLeaderPrim.objects.all()
    serializer_class = GroupLeaderPrimSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = GroupLeaderPrimFilter
    permission_classes = [maas_permissions.GroupLeaderPrimPermissions]

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            queryset = GroupLeaderPrim.objects.all()
        elif request.user.shirket is not None:
            queryset = GroupLeaderPrim.objects.filter(vezife__shirket=request.user.shirket)
        else:
            queryset = GroupLeaderPrim.objects.all()
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


class GroupLeaderPrimDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = GroupLeaderPrim.objects.all()
    serializer_class = GroupLeaderPrimSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = GroupLeaderPrimFilter
    permission_classes = [maas_permissions.GroupLeaderPrimPermissions]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "Van Leader bonus yeniləndi"}, status=status.HTTP_200_OK)

# ********************************** GroupLeader Prim New get post put delete **********************************
class GroupLeaderPrimNewListCreateAPIView(generics.ListCreateAPIView):
    queryset = GroupLeaderPrimNew.objects.all()
    serializer_class = GroupLeaderPrimNewSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = GroupLeaderPrimNewFilter
    permission_classes = [maas_permissions.GroupLeaderPrimNewPermissions]

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            queryset = GroupLeaderPrimNew.objects.all()
        elif request.user.shirket is not None:
            queryset = GroupLeaderPrimNew.objects.filter(vezife__shirket=request.user.shirket)
        else:
            queryset = GroupLeaderPrimNew.objects.all()
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
            prim = GroupLeaderPrimNew.objects.filter(prim_status=prim_status, vezife=vezife)
            if len(prim)>0:
                return Response({"detail": "Bu status və vəzifəyə uyğun prim artıq əlavə olunub"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                serializer.save()
                return Response({"detail": "Prim əlavə edildi"})


class GroupLeaderPrimNewDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = GroupLeaderPrimNew.objects.all()
    serializer_class = GroupLeaderPrimNewSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = GroupLeaderPrimNewFilter
    permission_classes = [maas_permissions.GroupLeaderPrimNewPermissions]

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

# ********************************** Menecer2 Prim get post put delete **********************************
class Menecer2PrimListCreateAPIView(generics.ListCreateAPIView):
    queryset = Menecer2Prim.objects.all()
    serializer_class = Menecer2PrimSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = Menecer2PrimFilter
    permission_classes = [maas_permissions.Menecer2PrimPermissions]

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            queryset = Menecer2Prim.objects.all()
        elif request.user.shirket is not None:
            queryset = Menecer2Prim.objects.filter(vezife__shirket=request.user.shirket)
        else:
            queryset = Menecer2Prim.objects.all()
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
            prim = Menecer2Prim.objects.filter(prim_status=prim_status, vezife=vezife)
            if len(prim)>0:
                return Response({"detail": "Bu status və vəzifəyə uyğun prim artıq əlavə olunub"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                serializer.save()
                return Response({"detail": "Prim əlavə edildi"})

class Menecer2PrimDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Menecer2Prim.objects.all()
    serializer_class = Menecer2PrimSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = Menecer2PrimFilter
    permission_classes = [maas_permissions.Menecer2PrimPermissions]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "Menecer2 bonus yeniləndi"}, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"detail": "Əməliyyat yerinə yetirildi"}, status=status.HTTP_204_NO_CONTENT)

# ********************************** Menecer1 Prim get post put delete **********************************
class Menecer1PrimListCreateAPIView(generics.ListCreateAPIView):
    queryset = Menecer1Prim.objects.all()
    serializer_class = Menecer1PrimSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = Menecer1PrimFilter
    permission_classes = [maas_permissions.Menecer1PrimPermissions]

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            queryset = Menecer1Prim.objects.all()
        elif request.user.shirket is not None:
            queryset = Menecer1Prim.objects.filter(vezife__shirket=request.user.shirket)
        else:
            queryset = Menecer1Prim.objects.all()
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

class Menecer1PrimDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Menecer1Prim.objects.all()
    serializer_class = Menecer1PrimSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = Menecer1PrimFilter
    permission_classes = [maas_permissions.Menecer1PrimPermissions]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "Menecer1 bonus yeniləndi"}, status=status.HTTP_200_OK)
    
# ********************************** Menecer1 Prim New get post put delete **********************************
class Menecer1PrimNewListCreateAPIView(generics.ListCreateAPIView):
    queryset = Menecer1PrimNew.objects.all()
    serializer_class = Menecer1PrimNewSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = Menecer1PrimNewFilter
    permission_classes = [maas_permissions.Menecer1PrimNewPermissions]

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            queryset = Menecer1PrimNew.objects.all()
        elif request.user.shirket is not None:
            queryset = Menecer1PrimNew.objects.filter(vezife__shirket=request.user.shirket)
        else:
            queryset = Menecer1PrimNew.objects.all()
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
            prim = Menecer1PrimNew.objects.filter(prim_status=prim_status, vezife=vezife)
            if len(prim)>0:
                return Response({"detail": "Bu status və vəzifəyə uyğun prim artıq əlavə olunub"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                serializer.save()
                return Response({"detail": "Prim əlavə edildi"})

class Menecer1PrimNewDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Menecer1PrimNew.objects.all()
    serializer_class = Menecer1PrimNewSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = Menecer1PrimNewFilter
    permission_classes = [maas_permissions.Menecer1PrimNewPermissions]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "Menecer1 bonus yeniləndi"}, status=status.HTTP_200_OK)

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