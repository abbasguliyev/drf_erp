from rest_framework import status, generics
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.response import Response

from restAPI.transfer.serializers import (
    HoldingdenShirketlereTransferSerializer,
    ShirketdenHoldingeTransferSerializer,
    OfisdenShirketeTransferSerializer,
    ShirketdenOfislereTransferSerializer,
)

from transfer.models import (
    HoldingdenShirketlereTransfer,
    ShirketdenHoldingeTransfer,
    ShirketdenOfislereTransfer,
    OfisdenShirketeTransfer,
)

from restAPI.transfer import utils as kassa_transfer_utils

from restAPI.transfer.filters import (
    HoldingdenShirketlereTransferFilter,
    OfisdenShirketeTransferFilter,
    ShirketdenHoldingeTransferFilter,
    ShirketdenOfislereTransferFilter,
)

from restAPI.transfer import permissions as transfer_permissions

# ********************************** transfer put delete post get **********************************

class HoldingdenShirketlereTransferListCreateAPIView(generics.ListCreateAPIView):
    queryset = HoldingdenShirketlereTransfer.objects.all()
    serializer_class = HoldingdenShirketlereTransferSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = HoldingdenShirketlereTransferFilter
    permission_classes = [transfer_permissions.HoldingdenShirketlereTransferPermissions]

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            queryset = HoldingdenShirketlereTransfer.objects.all()
        elif request.user.shirket is not None:
            queryset = HoldingdenShirketlereTransfer.objects.filter(shirket_kassa__shirket=request.user.shirket)
        else:
            queryset = HoldingdenShirketlereTransfer.objects.all()
        queryset = self.filter_queryset(queryset)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        return kassa_transfer_utils.holding_shirket_transfer_create(self, request, *args, **kwargs)


class HoldingdenShirketlereTransferDetailAPIView(generics.RetrieveAPIView):
    queryset = HoldingdenShirketlereTransfer.objects.all()
    serializer_class = HoldingdenShirketlereTransferSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = HoldingdenShirketlereTransferFilter
    permission_classes = [transfer_permissions.HoldingdenShirketlereTransferPermissions]



# **********************************

class ShirketdenHoldingeTransferListCreateAPIView(generics.ListCreateAPIView):
    queryset = ShirketdenHoldingeTransfer.objects.all()
    serializer_class = ShirketdenHoldingeTransferSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ShirketdenHoldingeTransferFilter
    permission_classes = [transfer_permissions.ShirketdenHoldingeTransferPermissions]

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            queryset = ShirketdenHoldingeTransfer.objects.all()
        elif request.user.shirket is not None:
            queryset = ShirketdenHoldingeTransfer.objects.filter(shirket_kassa__shirket=request.user.shirket)
        else:
            queryset = ShirketdenHoldingeTransfer.objects.all()
        queryset = self.filter_queryset(queryset)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
        
    def create(self, request, *args, **kwargs):
        return kassa_transfer_utils.shirket_holding_transfer_create(self, request, *args, **kwargs)


class ShirketdenHoldingeTransferDetailAPIView(generics.RetrieveAPIView):
    queryset = ShirketdenHoldingeTransfer.objects.all()
    serializer_class = ShirketdenHoldingeTransferSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ShirketdenHoldingeTransferFilter
    permission_classes = [transfer_permissions.ShirketdenHoldingeTransferPermissions]



# **********************************

class OfisdenShirketeTransferListCreateAPIView(generics.ListCreateAPIView):
    queryset = OfisdenShirketeTransfer.objects.all()
    serializer_class = OfisdenShirketeTransferSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = OfisdenShirketeTransferFilter
    permission_classes = [transfer_permissions.OfisdenShirketeTransferPermissions]

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            queryset = OfisdenShirketeTransfer.objects.all()
        elif request.user.shirket is not None:
            if request.user.ofis is not None:
                queryset = OfisdenShirketeTransfer.objects.filter(ofis_kassa__ofis__shirket=request.user.shirket, ofis_kassa__ofis=request.user.ofis, shirket_kassa__shirket=request.user.shirket)
            queryset = OfisdenShirketeTransfer.objects.filter(ofis_kassa__ofis__shirket=request.user.shirket, shirket_kassa__shirket=request.user.shirket)
        else:
            queryset = OfisdenShirketeTransfer.objects.all()
        queryset = self.filter_queryset(queryset)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        return kassa_transfer_utils.ofis_shirket_transfer_create(self, request, *args, **kwargs)


class OfisdenShirketeTransferDetailAPIView(generics.RetrieveAPIView):
    queryset = OfisdenShirketeTransfer.objects.all()
    serializer_class = OfisdenShirketeTransferSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = OfisdenShirketeTransferFilter
    permission_classes = [transfer_permissions.OfisdenShirketeTransferPermissions]



# **********************************

class ShirketdenOfislereTransferListCreateAPIView(generics.ListCreateAPIView):
    queryset = ShirketdenOfislereTransfer.objects.all()
    serializer_class = ShirketdenOfislereTransferSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ShirketdenOfislereTransferFilter
    permission_classes = [transfer_permissions.ShirketdenOfislereTransferPermissions]

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            queryset = ShirketdenOfislereTransfer.objects.all()
        elif request.user.shirket is not None:
            if request.user.ofis is not None:
                queryset = ShirketdenOfislereTransfer.objects.filter(ofis_kassa__ofis__shirket=request.user.shirket, ofis_kassa__ofis=request.user.ofis, shirket_kassa__shirket=request.user.shirket)
            queryset = ShirketdenOfislereTransfer.objects.filter(ofis_kassa__ofis__shirket=request.user.shirket, shirket_kassa__shirket=request.user.shirket)
        else:
            queryset = ShirketdenOfislereTransfer.objects.all()
        queryset = self.filter_queryset(queryset)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        return kassa_transfer_utils.shirket_ofis_transfer_create(self, request, *args, **kwargs)


class ShirketdenOfislereTransferDetailAPIView(generics.RetrieveAPIView):
    queryset = ShirketdenOfislereTransfer.objects.all()
    serializer_class = ShirketdenOfislereTransferSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ShirketdenOfislereTransferFilter
    permission_classes = [transfer_permissions.ShirketdenOfislereTransferPermissions]
