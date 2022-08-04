from rest_framework import status, generics
from rest_framework.response import Response
from restAPI.v1.services.serializers import (
    ServisOdemeSerializer,
    ServisSerializer,
)

from services.models import (
    Servis,
    ServisOdeme, 
)
from restAPI.v1.services import utils as servis_utils

from django_filters.rest_framework import DjangoFilterBackend

from restAPI.v1.services.filters import (
    ServisFilter,
    ServisOdemeFilter,
)

from restAPI.v1.services import permissions as muqavile_permissions

# ********************************** servis put delete post get **********************************

class ServisListCreateAPIView(generics.ListCreateAPIView):
    queryset = Servis.objects.all()
    serializer_class = ServisSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ServisFilter
    permission_classes = [muqavile_permissions.ServisPermissions]

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            queryset = Servis.objects.all()
        elif request.user.shirket is not None:
            if request.user.ofis is not None:
                queryset = Servis.objects.filter(muqavile__shirket=request.user.shirket, muqavile__ofis=request.user.ofis)
            queryset = Servis.objects.filter(muqavile__shirket=request.user.shirket)
        else:
            queryset = Servis.objects.all()
        
        queryset = self.filter_queryset(queryset)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        return servis_utils.servis_create(self, request, *args, **kwargs)


class ServisDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Servis.objects.all()
    serializer_class = ServisSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ServisFilter
    permission_classes = [muqavile_permissions.ServisPermissions]

    def update(self, request, *args, **kwargs):
        return servis_utils.servis_update(self, request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"detail": "Əməliyyat yerinə yetirildi"}, status=status.HTTP_204_NO_CONTENT)

# ********************************** servis odeme put delete post get **********************************

class ServisOdemeListCreateAPIView(generics.ListCreateAPIView):
    queryset = ServisOdeme.objects.all()
    serializer_class = ServisOdemeSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ServisOdemeFilter
    permission_classes = [muqavile_permissions.ServisPermissions]

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            queryset = ServisOdeme.objects.all()
        elif request.user.shirket is not None:
            if request.user.ofis is not None:
                queryset = ServisOdeme.objects.filter(servis__muqavile__shirket=request.user.shirket, servis__muqavile__ofis=request.user.ofis)
            queryset = ServisOdeme.objects.filter(servis__muqavile__shirket=request.user.shirket)
        else:
            queryset = ServisOdeme.objects.all()
        
        queryset = self.filter_queryset(queryset)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class ServisOdemeDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ServisOdeme.objects.all()
    serializer_class = ServisOdemeSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ServisOdemeFilter
    permission_classes = [muqavile_permissions.ServisPermissions]

    def update(self, request, *args, **kwargs):
        return servis_utils.servis_odeme_update(self, request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"detail": "Əməliyyat yerinə yetirildi"}, status=status.HTTP_204_NO_CONTENT)
