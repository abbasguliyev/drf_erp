from rest_framework import status, generics
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.response import Response

from restAPI.income_expense.serializers import (
    OfisKassaMedaxilSerializer,
    OfisKassaMexaricSerializer,
    ShirketKassaMedaxilSerializer,
    ShirketKassaMexaricSerializer,
    HoldingKassaMedaxilSerializer,
    HoldingKassaMexaricSerializer
)


from income_expense.models import (
    HoldingKassaMedaxil,
    HoldingKassaMexaric,
    OfisKassaMedaxil,
    OfisKassaMexaric,
    ShirketKassaMedaxil,
    ShirketKassaMexaric,
)

from restAPI.income_expense import utils as medaxil_mexaric_utils
from restAPI.income_expense.filters import (
    HoldingKassaMedaxilFilter,
    HoldingKassaMexaricFilter,
    OfisKassaMedaxilFilter,
    OfisKassaMexaricFilter,
    ShirketKassaMedaxilFilter,
    ShirketKassaMexaricFilter,
)

from restAPI.income_expense import permissions as company_permissions

# ********************************** holding kassa medaxil, mexaric put delete post get **********************************

class HoldingKassaMedaxilListCreateAPIView(generics.ListCreateAPIView):
    queryset = HoldingKassaMedaxil.objects.all()
    serializer_class = HoldingKassaMedaxilSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = HoldingKassaMedaxilFilter
    permission_classes = [company_permissions.HoldingKassaMedaxilPermissions]

    def create(self, request, *args, **kwargs):
        return medaxil_mexaric_utils.holding_kassa_medaxil_create(self, request, *args, **kwargs)


class HoldingKassaMedaxilDetailAPIView(generics.RetrieveAPIView):
    queryset = HoldingKassaMedaxil.objects.all()
    serializer_class = HoldingKassaMedaxilSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = HoldingKassaMedaxilFilter
    permission_classes = [company_permissions.HoldingKassaMedaxilPermissions]



# **********************************

class HoldingKassaMexaricListCreateAPIView(generics.ListCreateAPIView):
    queryset = HoldingKassaMexaric.objects.all()
    serializer_class = HoldingKassaMexaricSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = HoldingKassaMexaricFilter
    permission_classes = [company_permissions.HoldingKassaMexaricPermissions]

    def create(self, request, *args, **kwargs):
        return medaxil_mexaric_utils.holding_kassa_mexaric_create(self, request, *args, **kwargs)


class HoldingKassaMexaricDetailAPIView(generics.RetrieveAPIView):
    queryset = HoldingKassaMexaric.objects.all()
    serializer_class = HoldingKassaMexaricSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = HoldingKassaMexaricFilter
    permission_classes = [company_permissions.HoldingKassaMexaricPermissions]



# ********************************** shirket kassa medaxil, mexaric put delete post get **********************************

class ShirketKassaMedaxilListCreateAPIView(generics.ListCreateAPIView):
    queryset = ShirketKassaMedaxil.objects.all()
    serializer_class = ShirketKassaMedaxilSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ShirketKassaMedaxilFilter
    permission_classes = [company_permissions.ShirketKassaMedaxilPermissions]

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            queryset = ShirketKassaMedaxil.objects.all()
        elif request.user.shirket is not None:
            queryset = ShirketKassaMedaxil.objects.filter(shirket_kassa__shirket=request.user.shirket)
        else:
            queryset = ShirketKassaMedaxil.objects.all()
        queryset = self.filter_queryset(queryset)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


    def create(self, request, *args, **kwargs):
        return medaxil_mexaric_utils.shirket_kassa_medaxil_create(self, request, *args, **kwargs)


class ShirketKassaMedaxilDetailAPIView(generics.RetrieveAPIView):
    queryset = ShirketKassaMedaxil.objects.all()
    serializer_class = ShirketKassaMedaxilSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ShirketKassaMedaxilFilter
    permission_classes = [company_permissions.ShirketKassaMedaxilPermissions]



# **********************************

class ShirketKassaMexaricListCreateAPIView(generics.ListCreateAPIView):
    queryset = ShirketKassaMexaric.objects.all()
    serializer_class = ShirketKassaMexaricSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ShirketKassaMexaricFilter
    permission_classes = [company_permissions.ShirketKassaMexaricPermissions]

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            queryset = ShirketKassaMexaric.objects.all()
        elif request.user.shirket is not None:
            queryset = ShirketKassaMexaric.objects.filter(shirket_kassa__shirket=request.user.shirket)
        else:
            queryset = ShirketKassaMexaric.objects.all()
        queryset = self.filter_queryset(queryset)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        return medaxil_mexaric_utils.shirket_kassa_mexaric_create(self, request, *args, **kwargs)


class ShirketKassaMexaricDetailAPIView(generics.RetrieveAPIView):
    queryset = ShirketKassaMexaric.objects.all()
    serializer_class = ShirketKassaMexaricSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ShirketKassaMexaricFilter
    permission_classes = [company_permissions.ShirketKassaMexaricPermissions]



# ********************************** Ofis kassa medaxil, mexaric put delete post get **********************************

class OfisKassaMedaxilListCreateAPIView(generics.ListCreateAPIView):
    queryset = OfisKassaMedaxil.objects.all()
    serializer_class = OfisKassaMedaxilSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = OfisKassaMedaxilFilter
    permission_classes = [company_permissions.OfisKassaMedaxilPermissions]

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            queryset = OfisKassaMedaxil.objects.all()
        elif request.user.shirket is not None:
            if request.user.ofis is not None:
                queryset = OfisKassaMedaxil.objects.filter(ofis_kassa__ofis__shirket=request.user.shirket, ofis_kassa__ofis=request.user.ofis)
            queryset = OfisKassaMedaxil.objects.filter(ofis_kassa__ofis__shirket=request.user.shirket)
        else:
            queryset = OfisKassaMedaxil.objects.all()
        queryset = self.filter_queryset(queryset)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        return medaxil_mexaric_utils.ofis_kassa_medaxil_create(self, request, *args, **kwargs)


class OfisKassaMedaxilDetailAPIView(generics.RetrieveAPIView):
    queryset = OfisKassaMedaxil.objects.all()
    serializer_class = OfisKassaMedaxilSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = OfisKassaMedaxilFilter
    permission_classes = [company_permissions.OfisKassaMedaxilPermissions]



# **********************************

class OfisKassaMexaricListCreateAPIView(generics.ListCreateAPIView):
    queryset = OfisKassaMexaric.objects.all()
    serializer_class = OfisKassaMexaricSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = OfisKassaMexaricFilter
    permission_classes = [company_permissions.OfisKassaMexaricPermissions]

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            queryset = OfisKassaMexaric.objects.all()
        elif request.user.shirket is not None:
            if request.user.ofis is not None:
                queryset = OfisKassaMexaric.objects.filter(ofis_kassa__ofis__shirket=request.user.shirket, ofis_kassa__ofis=request.user.ofis)
            queryset = OfisKassaMexaric.objects.filter(ofis_kassa__ofis__shirket=request.user.shirket)
        else:
            queryset = OfisKassaMexaric.objects.all()
        queryset = self.filter_queryset(queryset)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        return medaxil_mexaric_utils.ofis_kassa_mexaric_create(self, request, *args, **kwargs)


class OfisKassaMexaricDetailAPIView(generics.RetrieveAPIView):
    queryset = OfisKassaMexaric.objects.all()
    serializer_class = OfisKassaMexaricSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = OfisKassaMexaricFilter
    permission_classes = [company_permissions.OfisKassaMexaricPermissions]
