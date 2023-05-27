from rest_framework import status, generics, permissions
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.response import Response

from update.api.serializers import UpdateSerializer
from update.models import Update

from update.api.filters import UpdateFilter

from core.utils.permission_utils import IsAdminUserOrReadOnly


class UpdateListCreateAPIView(generics.ListCreateAPIView):
    queryset = Update.objects.all()
    serializer_class = UpdateSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = UpdateFilter
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({"detail": "Update əlavə edildi"}, status=status.HTTP_201_CREATED, headers=headers)


class UpdateDetailAPIView(generics.RetrieveUpdateAPIView):
    queryset = Update.objects.all()
    serializer_class = UpdateSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = UpdateFilter
    permission_classes = [permissions.AllowAny]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({"detail": "Məlumatlar yeniləndi"})
