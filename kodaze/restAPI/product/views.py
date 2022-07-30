import datetime
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework import generics
from restAPI.product.serializers import (
    MehsullarSerializer,
)
from product.models import (
    Mehsullar, 
)
from django_filters.rest_framework import DjangoFilterBackend
from restAPI.product.filters import (
    MehsullarFilter,
)
from restAPI.product import permissions as muqavile_permissions

# ********************************** mehsullar put get post delete **********************************

class MehsullarListCreateAPIView(generics.ListCreateAPIView):
    queryset = Mehsullar.objects.all()
    serializer_class = MehsullarSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = MehsullarFilter
    permission_classes = [muqavile_permissions.MehsullarPermissions]

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            queryset = Mehsullar.objects.all()
        elif request.user.shirket is not None:
            queryset = Mehsullar.objects.filter(shirket=request.user.shirket)
        else:
            queryset = Mehsullar.objects.all()
        
        queryset = self.filter_queryset(queryset)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({"detail": "Məhsul əlavə edildi"}, status=status.HTTP_201_CREATED, headers=headers)


class MehsullarDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Mehsullar.objects.all()
    serializer_class = MehsullarSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = MehsullarFilter
    permission_classes = [muqavile_permissions.MehsullarPermissions]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response({"detail": "Məhsul məlumatları yeniləndi"}, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"detail": "Əməliyyat yerinə yetirildi"}, status=status.HTTP_204_NO_CONTENT)
