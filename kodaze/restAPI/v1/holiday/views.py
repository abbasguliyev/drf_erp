from restAPI.v1.holiday.serializers import (
    HoldingGunlerSerializer,
    IsciGelibGetmeVaxtlariSerializer, 
    IsciGunlerSerializer, 
    KomandaGunlerSerializer,
    KomandaIstisnaIsciSerializer, 
    OfisGunlerSerializer,
    OfisIstisnaIsciSerializer, 
    ShirketGunlerSerializer,
    ShirketIstisnaIsciSerializer, 
    ShobeGunlerSerializer,
    ShobeIstisnaIsciSerializer, 
    VezifeGunlerSerializer,
    HoldingIstisnaIsciSerializer,
    VezifeIstisnaIsciSerializer
)
from holiday.models import (
    HoldingGunler,
    IsciGelibGetmeVaxtlari,
    IsciGunler,
    KomandaGunler,
    KomandaIstisnaIsci,
    OfisGunler,
    OfisIstisnaIsci,
    ShirketGunler,
    ShirketIstisnaIsci,
    ShobeGunler,
    ShobeIstisnaIsci,
    VezifeGunler,
    HoldingIstisnaIsci,
    VezifeIstisnaIsci
)

from rest_framework.response import Response

from restAPI.v1.holiday import utils as gunler_utils

from rest_framework import generics

from restAPI.v1.holiday import permissions as gunler_permissions

from django_filters.rest_framework import DjangoFilterBackend

from restAPI.v1.holiday.filters import (
    HoldingGunlerFilter,
    HoldingIstisnaIsciFilter,
    IsciGelibGetmeVaxtlariFilter,
    IsciGunlerFilter,
    KomandaGunlerFilter,
    KomandaIstisnaIsciFilter,
    OfisGunlerFilter,
    OfisIstisnaIsciFilter,
    ShirketGunlerFilter,
    ShirketIstisnaIsciFilter,
    ShobeGunlerFilter,
    ShobeIstisnaIsciFilter,
    VezifeGunlerFilter,
    VezifeIstisnaIsciFilter,
) 
from rest_framework import status

# ********************************** Holding Gunler get post put delete **********************************
class HoldingGunlerListCreateAPIView(generics.ListAPIView):
    queryset = HoldingGunler.objects.all()
    serializer_class = HoldingGunlerSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = HoldingGunlerFilter
    permission_classes = [gunler_permissions.HoldingGunlerPermissions]

class HoldingGunlerDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = HoldingGunler.objects.all()
    serializer_class = HoldingGunlerSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = HoldingGunlerFilter
    permission_classes = [gunler_permissions.HoldingGunlerPermissions]

    def update(self, request, *args, **kwargs):
        return gunler_utils.holding_gunler_update(self, request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"detail": "Əməliyyat yerinə yetirildi"}, status=status.HTTP_204_NO_CONTENT)

class HoldingIstisnaIsciListCreateAPIView(generics.ListCreateAPIView):
    queryset = HoldingIstisnaIsci.objects.all()
    serializer_class = HoldingIstisnaIsciSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = HoldingIstisnaIsciFilter
    permission_classes = [gunler_permissions.HoldingIstisnaIsciPermissions]

    def create(self, request, *args, **kwargs):
        return gunler_utils.holding_istisna_isci_gunler_create(self, request, *args, **kwargs)

class HoldingIstisnaIsciDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = HoldingIstisnaIsci.objects.all()
    serializer_class = HoldingIstisnaIsciSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = HoldingIstisnaIsciFilter
    permission_classes = [gunler_permissions.HoldingIstisnaIsciPermissions]

    def update(self, request, *args, **kwargs):
        return gunler_utils.holding_istisna_isci_gunler_update(self, request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return gunler_utils.holding_istisna_isci_gunler_delete(self, request, *args, **kwargs)

# ********************************** Shirket Gunler get post put delete **********************************
class ShirketGunlerListCreateAPIView(generics.ListAPIView):
    queryset = ShirketGunler.objects.all()
    serializer_class = ShirketGunlerSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ShirketGunlerFilter
    permission_classes = [gunler_permissions.ShirketGunlerPermissions]

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            queryset = ShirketGunler.objects.all()
        elif request.user.shirket is not None:
            queryset = ShirketGunler.objects.filter(shirket=request.user.shirket)
        else:
            queryset = ShirketGunler.objects.all()
        queryset = self.filter_queryset(queryset)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ShirketGunlerDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ShirketGunler.objects.all()
    serializer_class = ShirketGunlerSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ShirketGunlerFilter
    permission_classes = [gunler_permissions.ShirketGunlerPermissions]

    def update(self, request, *args, **kwargs):
        return gunler_utils.shirket_gunler_update(self, request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"detail": "Əməliyyat yerinə yetirildi"}, status=status.HTTP_204_NO_CONTENT)

class ShirketIstisnaIsciListCreateAPIView(generics.ListCreateAPIView):
    queryset = ShirketIstisnaIsci.objects.all()
    serializer_class = ShirketIstisnaIsciSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ShirketIstisnaIsciFilter
    permission_classes = [gunler_permissions.ShirketIstisnaIsciPermissions]

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            queryset = ShirketIstisnaIsci.objects.all()
        elif request.user.shirket is not None:
            queryset = ShirketIstisnaIsci.objects.filter(gunler__shirket=request.user.shirket)
        else:
            queryset = ShirketIstisnaIsci.objects.all()
        queryset = self.filter_queryset(queryset)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        return gunler_utils.shirket_istisna_isci_gunler_create(self, request, *args, **kwargs)

class ShirketIstisnaIsciDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ShirketIstisnaIsci.objects.all()
    serializer_class = ShirketIstisnaIsciSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ShirketIstisnaIsciFilter
    permission_classes = [gunler_permissions.ShirketIstisnaIsciPermissions]

    def update(self, request, *args, **kwargs):
        return gunler_utils.shirket_istisna_isci_gunler_update(self, request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return gunler_utils.shirket_istisna_isci_gunler_delete(self, request, *args, **kwargs)

# ********************************** Ofis Gunler get post put delete **********************************
class OfisGunlerListCreateAPIView(generics.ListAPIView):
    queryset = OfisGunler.objects.all()
    serializer_class = OfisGunlerSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = OfisGunlerFilter
    permission_classes = [gunler_permissions.OfisGunlerPermissions]

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            queryset = OfisGunler.objects.all()
        elif request.user.shirket is not None:
            if request.user.ofis is not None:
                queryset = OfisGunler.objects.filter(ofis__shirket=request.user.shirket, ofis=request.user.ofis)
            queryset = OfisGunler.objects.filter(ofis__shirket=request.user.shirket)
        else:
            queryset = OfisGunler.objects.all()
        queryset = self.filter_queryset(queryset)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class OfisGunlerDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = OfisGunler.objects.all()
    serializer_class = OfisGunlerSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = OfisGunlerFilter
    permission_classes = [gunler_permissions.OfisGunlerPermissions]

    def update(self, request, *args, **kwargs):
        return gunler_utils.ofis_gunler_update(self, request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"detail": "Əməliyyat yerinə yetirildi"}, status=status.HTTP_204_NO_CONTENT)

class OfisIstisnaIsciListCreateAPIView(generics.ListCreateAPIView):
    queryset = OfisIstisnaIsci.objects.all()
    serializer_class = OfisIstisnaIsciSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = OfisIstisnaIsciFilter
    permission_classes = [gunler_permissions.OfisIstisnaIsciPermissions]

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            queryset = OfisIstisnaIsci.objects.all()
        elif request.user.shirket is not None:
            if request.user.ofis is not None:
                queryset = OfisIstisnaIsci.objects.filter(gunler__ofis__shirket=request.user.shirket, gunler__ofis=request.user.ofis)
            queryset = OfisIstisnaIsci.objects.filter(gunler__ofis__shirket=request.user.shirket)
        else:
            queryset = OfisIstisnaIsci.objects.all()
        queryset = self.filter_queryset(queryset)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        return gunler_utils.ofis_istisna_isci_gunler_create(self, request, *args, **kwargs)

class OfisIstisnaIsciDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = OfisIstisnaIsci.objects.all()
    serializer_class = OfisIstisnaIsciSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = OfisIstisnaIsciFilter
    permission_classes = [gunler_permissions.OfisIstisnaIsciPermissions]

    def update(self, request, *args, **kwargs):
        return gunler_utils.ofis_istisna_isci_gunler_update(self, request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return gunler_utils.ofis_istisna_isci_gunler_delete(self, request, *args, **kwargs)

# ********************************** Shobe Gunler get post put delete **********************************
class ShobeGunlerListCreateAPIView(generics.ListAPIView):
    queryset = ShobeGunler.objects.all()
    serializer_class = ShobeGunlerSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ShobeGunlerFilter
    permission_classes = [gunler_permissions.ShobeGunlerPermissions]

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            queryset = ShobeGunler.objects.all()
        elif request.user.shirket is not None:
            if request.user.ofis is not None:
                queryset = ShobeGunler.objects.filter(shobe__ofis__shirket=request.user.shirket, shobe__ofis=request.user.ofis)
            queryset = ShobeGunler.objects.filter(shobe__ofis__shirket=request.user.shirket)
        else:
            queryset = ShobeGunler.objects.all()
        queryset = self.filter_queryset(queryset)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ShobeGunlerDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ShobeGunler.objects.all()
    serializer_class = ShobeGunlerSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ShobeGunlerFilter
    permission_classes = [gunler_permissions.ShobeGunlerPermissions]

    def update(self, request, *args, **kwargs):
        return gunler_utils.shobe_gunler_update(self, request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"detail": "Əməliyyat yerinə yetirildi"}, status=status.HTTP_204_NO_CONTENT)

class ShobeIstisnaIsciListCreateAPIView(generics.ListCreateAPIView):
    queryset = ShobeIstisnaIsci.objects.all()
    serializer_class = ShobeIstisnaIsciSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ShobeIstisnaIsciFilter
    permission_classes = [gunler_permissions.ShobeIstisnaIsciPermissions]

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            queryset = ShobeIstisnaIsci.objects.all()
        elif request.user.shirket is not None:
            if request.user.ofis is not None:
                queryset = ShobeIstisnaIsci.objects.filter(gunler__shobe__ofis__shirket=request.user.shirket, gunler__shobe__ofis=request.user.ofis)
            queryset = ShobeIstisnaIsci.objects.filter(gunler__shobe__ofis__shirket=request.user.shirket)
        else:
            queryset = ShobeIstisnaIsci.objects.all()
        queryset = self.filter_queryset(queryset)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        return gunler_utils.shobe_istisna_isci_gunler_create(self, request, *args, **kwargs)

class ShobeIstisnaIsciDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ShobeIstisnaIsci.objects.all()
    serializer_class = ShobeIstisnaIsciSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ShobeIstisnaIsciFilter
    permission_classes = [gunler_permissions.ShobeIstisnaIsciPermissions]

    def update(self, request, *args, **kwargs):
        return gunler_utils.shobe_istisna_isci_gunler_update(self, request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return gunler_utils.shobe_istisna_isci_gunler_delete(self, request, *args, **kwargs)

# ********************************** Komanda Gunler get post put delete **********************************
class KomandaGunlerListCreateAPIView(generics.ListAPIView):
    queryset = KomandaGunler.objects.all()
    serializer_class = KomandaGunlerSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = KomandaGunlerFilter
    permission_classes = [gunler_permissions.KomandaGunlerPermissions]


class KomandaGunlerDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = KomandaGunler.objects.all()
    serializer_class = KomandaGunlerSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = KomandaGunlerFilter
    permission_classes = [gunler_permissions.KomandaGunlerPermissions]

    def update(self, request, *args, **kwargs):
        return gunler_utils.komanda_gunler_update(self, request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"detail": "Əməliyyat yerinə yetirildi"}, status=status.HTTP_204_NO_CONTENT)

class KomandaIstisnaIsciListCreateAPIView(generics.ListCreateAPIView):
    queryset = KomandaIstisnaIsci.objects.all()
    serializer_class = KomandaIstisnaIsciSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = KomandaIstisnaIsciFilter
    permission_classes = [gunler_permissions.KomandaIstisnaIsciPermissions]

    def create(self, request, *args, **kwargs):
        return gunler_utils.komanda_istisna_isci_gunler_create(self, request, *args, **kwargs)

class KomandaIstisnaIsciDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = KomandaIstisnaIsci.objects.all()
    serializer_class = KomandaIstisnaIsciSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = KomandaIstisnaIsciFilter
    permission_classes = [gunler_permissions.KomandaIstisnaIsciPermissions]

    def update(self, request, *args, **kwargs):
        return gunler_utils.komanda_istisna_isci_gunler_update(self, request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return gunler_utils.komanda_istisna_isci_gunler_delete(self, request, *args, **kwargs)

# ********************************** Vezife Gunler get post put delete **********************************
class VezifeGunlerListCreateAPIView(generics.ListAPIView):
    queryset = VezifeGunler.objects.all()
    serializer_class = VezifeGunlerSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = VezifeGunlerFilter
    permission_classes = [gunler_permissions.VezifeGunlerPermissions]

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            queryset = VezifeGunler.objects.all()
        elif request.user.shirket is not None:
            queryset = VezifeGunler.objects.filter(vezife__shirket=request.user.shirket)
        else:
            queryset = VezifeGunler.objects.all()
        queryset = self.filter_queryset(queryset)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class VezifeGunlerDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = VezifeGunler.objects.all()
    serializer_class = VezifeGunlerSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = VezifeGunlerFilter
    permission_classes = [gunler_permissions.VezifeGunlerPermissions]

    def update(self, request, *args, **kwargs):
        return gunler_utils.vezife_gunler_update(self, request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"detail": "Əməliyyat yerinə yetirildi"}, status=status.HTTP_204_NO_CONTENT)

class VezifeIstisnaIsciListCreateAPIView(generics.ListCreateAPIView):
    queryset = VezifeIstisnaIsci.objects.all()
    serializer_class = VezifeIstisnaIsciSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = VezifeIstisnaIsciFilter
    permission_classes = [gunler_permissions.VezifeIstisnaIsciPermissions]

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            queryset = VezifeIstisnaIsci.objects.all()
        elif request.user.shirket is not None:
            queryset = VezifeIstisnaIsci.objects.filter(gunler__vezife__shirket=request.user.shirket)
        else:
            queryset = VezifeIstisnaIsci.objects.all()
        queryset = self.filter_queryset(queryset)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        return gunler_utils.vezife_istisna_isci_gunler_create(self, request, *args, **kwargs)

class VezifeIstisnaIsciDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = VezifeIstisnaIsci.objects.all()
    serializer_class = VezifeIstisnaIsciSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = VezifeIstisnaIsciFilter
    permission_classes = [gunler_permissions.VezifeIstisnaIsciPermissions]

    def update(self, request, *args, **kwargs):
        return gunler_utils.vezife_istisna_isci_gunler_update(self, request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return gunler_utils.vezife_istisna_isci_gunler_delete(self, request, *args, **kwargs)
    
# ********************************** Isci Gunler get post put delete **********************************
class IsciGunlerListCreateAPIView(generics.ListAPIView):
    queryset = IsciGunler.objects.all()
    serializer_class = IsciGunlerSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = IsciGunlerFilter
    permission_classes = [gunler_permissions.IsciGunlerPermissions]

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            queryset = IsciGunler.objects.all()
        elif request.user.shirket is not None:
            if request.user.ofis is not None:
                queryset = IsciGunler.objects.filter(isci__shirket=request.user.shirket, isci__ofis=request.user.ofis)
            queryset = IsciGunler.objects.filter(isci__shirket=request.user.shirket)
        else:
            queryset = IsciGunler.objects.all()
        queryset = self.filter_queryset(queryset)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class IsciGunlerDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = IsciGunler.objects.all()
    serializer_class = IsciGunlerSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = IsciGunlerFilter
    permission_classes = [gunler_permissions.IsciGunlerPermissions]

    def update(self, request, *args, **kwargs):
        return gunler_utils.user_gunler_update(self, request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return gunler_utils.user_gunler_patch(self, request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return gunler_utils.user_gunler_delete(self, request, *args, **kwargs)

# ********************************** Isci Gelib getme vaxtlari get post put delete **********************************
class IsciGelibGetmeVaxtlariListCreateAPIView(generics.ListCreateAPIView):
    queryset = IsciGelibGetmeVaxtlari.objects.all()
    serializer_class = IsciGelibGetmeVaxtlariSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = IsciGelibGetmeVaxtlariFilter
    permission_classes = [gunler_permissions.IsciGelibGetmeVaxtlariPermissions]

class IsciGelibGetmeVaxtlariDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = IsciGelibGetmeVaxtlari.objects.all()
    serializer_class = IsciGelibGetmeVaxtlariSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = IsciGelibGetmeVaxtlariFilter
    permission_classes = [gunler_permissions.IsciGelibGetmeVaxtlariPermissions]
