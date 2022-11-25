from rest_framework import status, generics
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.response import Response

from transfer.api.serializers import (
    HoldingTransferSerializer,
    CompanyTransferSerializer,
    OfficeTransferSerializer,
)

from transfer.models import (
    HoldingTransfer,
    CompanyTransfer,
    OfficeTransfer,
)

from transfer.api.filters import (
    HoldingTransferFilter,
    CompanyTransferFilter,
    OfficeTransferFilter,
)

from transfer.api.services import (
    holding_transfer_services,
    company_transfer_services,
    office_transfer_services
)

from transfer.api.selectors import (
    holding_transfer_list,
    company_transfer_list,
    office_transfer_list
)

from transfer.api import permissions as transfer_permissions

class HoldingTransferListCreateAPIView(generics.ListCreateAPIView):
    queryset = holding_transfer_list()
    serializer_class = HoldingTransferSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = HoldingTransferFilter
    permission_classes = [transfer_permissions.HoldingTransferPermissions]

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            queryset = self.queryset
        elif request.user.company is not None:
            queryset = self.queryset.filter(sending_company=request.user.company)
        else:
            queryset = self.queryset
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
        if(serializer.is_valid()):
            holding_transfer_services.holding_transfer_create(user=user, **serializer.validated_data)
            return Response({"detail": "Transfer yerinə yetirildi"}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class CompanyTransferListCreateAPIView(generics.ListCreateAPIView):
    queryset = company_transfer_list()
    serializer_class = CompanyTransferSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CompanyTransferFilter
    permission_classes = [transfer_permissions.CompanyTransferPermissions]

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            queryset = self.queryset
        elif request.user.company is not None:
            queryset = self.queryset.filter(company=request.user.company)
        else:
            queryset = self.queryset
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
        if(serializer.is_valid()):
            company_transfer_services.company_transfer_create(user=user, **serializer.validated_data)
            return Response({"detail": "Transfer yerinə yetirildi"}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class OfficeTransferListCreateAPIView(generics.ListCreateAPIView):
    queryset = office_transfer_list()
    serializer_class = OfficeTransferSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = OfficeTransferFilter
    permission_classes = [transfer_permissions.OfficeTransferPermissions]

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            queryset = self.queryset
        elif request.user.company is not None:
            queryset = self.queryset.filter(company=request.user.company)
        else:
            queryset = self.queryset
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
        if(serializer.is_valid()):
            office_transfer_services.office_transfer_create(user=user, **serializer.validated_data)
            return Response({"detail": "Transfer yerinə yetirildi"}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)