from rest_framework import status, generics
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.response import Response

from restAPI.v1.transfer.serializers import (
    TransferFromHoldingToCompanySerializer,
    TransferFromCompanyToHoldingSerializer,
    TransferFromOfficeToCompanySerializer,
    TransferFromCompanyToOfficesSerializer,
)

from transfer.models import (
    TransferFromHoldingToCompany,
    TransferFromCompanyToHolding,
    TransferFromCompanyToOffices,
    TransferFromOfficeToCompany,
)

from restAPI.v1.transfer import utils as kassa_transfer_utils

from restAPI.v1.transfer.filters import (
    TransferFromHoldingToCompanyFilter,
    TransferFromOfficeToCompanyFilter,
    TransferFromCompanyToHoldingFilter,
    TransferFromCompanyToOfficesFilter,
)

from restAPI.v1.transfer import permissions as transfer_permissions

# ********************************** transfer put delete post get **********************************

class TransferFromHoldingToCompanyListCreateAPIView(generics.ListCreateAPIView):
    queryset = TransferFromHoldingToCompany.objects.all()
    serializer_class = TransferFromHoldingToCompanySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = TransferFromHoldingToCompanyFilter
    permission_classes = [transfer_permissions.TransferFromHoldingToCompanyPermissions]

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            queryset = TransferFromHoldingToCompany.objects.all()
        elif request.user.company is not None:
            queryset = TransferFromHoldingToCompany.objects.filter(cashbox__company=request.user.company)
        else:
            queryset = TransferFromHoldingToCompany.objects.all()
        queryset = self.filter_queryset(queryset)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        return kassa_transfer_utils.holding_company_transfer_create(self, request, *args, **kwargs)


class TransferFromHoldingToCompanyDetailAPIView(generics.RetrieveAPIView):
    queryset = TransferFromHoldingToCompany.objects.all()
    serializer_class = TransferFromHoldingToCompanySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = TransferFromHoldingToCompanyFilter
    permission_classes = [transfer_permissions.TransferFromHoldingToCompanyPermissions]



# **********************************

class TransferFromCompanyToHoldingListCreateAPIView(generics.ListCreateAPIView):
    queryset = TransferFromCompanyToHolding.objects.all()
    serializer_class = TransferFromCompanyToHoldingSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = TransferFromCompanyToHoldingFilter
    permission_classes = [transfer_permissions.TransferFromCompanyToHoldingPermissions]

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            queryset = TransferFromCompanyToHolding.objects.all()
        elif request.user.company is not None:
            queryset = TransferFromCompanyToHolding.objects.filter(cashbox__company=request.user.company)
        else:
            queryset = TransferFromCompanyToHolding.objects.all()
        queryset = self.filter_queryset(queryset)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
        
    def create(self, request, *args, **kwargs):
        return kassa_transfer_utils.company_holding_transfer_create(self, request, *args, **kwargs)


class TransferFromCompanyToHoldingDetailAPIView(generics.RetrieveAPIView):
    queryset = TransferFromCompanyToHolding.objects.all()
    serializer_class = TransferFromCompanyToHoldingSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = TransferFromCompanyToHoldingFilter
    permission_classes = [transfer_permissions.TransferFromCompanyToHoldingPermissions]



# **********************************

class TransferFromOfficeToCompanyListCreateAPIView(generics.ListCreateAPIView):
    queryset = TransferFromOfficeToCompany.objects.all()
    serializer_class = TransferFromOfficeToCompanySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = TransferFromOfficeToCompanyFilter
    permission_classes = [transfer_permissions.TransferFromOfficeToCompanyPermissions]

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            queryset = TransferFromOfficeToCompany.objects.all()
        elif request.user.company is not None:
            if request.user.office is not None:
                queryset = TransferFromOfficeToCompany.objects.filter(cashbox__office__company=request.user.company, cashbox__office=request.user.office, cashbox__company=request.user.company)
            queryset = TransferFromOfficeToCompany.objects.filter(cashbox__office__company=request.user.company, cashbox__company=request.user.company)
        else:
            queryset = TransferFromOfficeToCompany.objects.all()
        queryset = self.filter_queryset(queryset)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        return kassa_transfer_utils.office_company_transfer_create(self, request, *args, **kwargs)


class TransferFromOfficeToCompanyDetailAPIView(generics.RetrieveAPIView):
    queryset = TransferFromOfficeToCompany.objects.all()
    serializer_class = TransferFromOfficeToCompanySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = TransferFromOfficeToCompanyFilter
    permission_classes = [transfer_permissions.TransferFromOfficeToCompanyPermissions]



# **********************************

class TransferFromCompanyToOfficesListCreateAPIView(generics.ListCreateAPIView):
    queryset = TransferFromCompanyToOffices.objects.all()
    serializer_class = TransferFromCompanyToOfficesSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = TransferFromCompanyToOfficesFilter
    permission_classes = [transfer_permissions.TransferFromCompanyToOfficesPermissions]

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            queryset = TransferFromCompanyToOffices.objects.all()
        elif request.user.company is not None:
            if request.user.office is not None:
                queryset = TransferFromCompanyToOffices.objects.filter(cashbox__office__company=request.user.company, cashbox__office=request.user.office, cashbox__company=request.user.company)
            queryset = TransferFromCompanyToOffices.objects.filter(cashbox__office__company=request.user.company, cashbox__company=request.user.company)
        else:
            queryset = TransferFromCompanyToOffices.objects.all()
        queryset = self.filter_queryset(queryset)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        return kassa_transfer_utils.offices_transfer_create(self, request, *args, **kwargs)


class TransferFromCompanyToOfficesDetailAPIView(generics.RetrieveAPIView):
    queryset = TransferFromCompanyToOffices.objects.all()
    serializer_class = TransferFromCompanyToOfficesSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = TransferFromCompanyToOfficesFilter
    permission_classes = [transfer_permissions.TransferFromCompanyToOfficesPermissions]
