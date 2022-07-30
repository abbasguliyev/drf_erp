from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework import generics

from restAPI.warehouse.serializers import (
    AnbarSerializer,
    EmeliyyatSerializer,
    AnbarQeydlerSerializer,
    StokSerializer,
)

from warehouse.models import (
    Emeliyyat, 
    Anbar, 
    AnbarQeydler, 
    Stok
)
from restAPI.warehouse.utils import (
    anbar_emeliyyat_utils,
    stok_utils
)

from django_filters.rest_framework import DjangoFilterBackend

from restAPI.warehouse.filters import (
    AnbarFilter,
    AnbarQeydlerFilter,
    EmeliyyatFilter,
    StokFilter,
)

from restAPI.warehouse import permissions as muqavile_permissions

# ********************************** anbar put get post delete **********************************
class AnbarListCreateAPIView(generics.ListCreateAPIView):
    queryset = Anbar.objects.all()
    serializer_class = AnbarSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = AnbarFilter
    permission_classes = [muqavile_permissions.AnbarPermissions]

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            queryset = Anbar.objects.all()
        elif request.user.shirket is not None:
            if request.user.ofis is not None:
                queryset = Anbar.objects.filter(shirket=request.user.shirket, ofis=request.user.ofis)
            queryset = Anbar.objects.filter(shirket=request.user.shirket)
        else:
            queryset = Anbar.objects.all()
        
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
            ofis = serializer.validated_data.get("ofis")
            is_have_anbar = Anbar.objects.filter(ofis=ofis)
            if len(is_have_anbar) > 0:
                return Response({"detail":"Bir ofisin yalnız bir anbarı ola bilər!"}, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response({"detail":"Anbar quruldu"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"detail":"Məlumatları doğru daxil etdiyinizdən əmin olun"}, status=status.HTTP_400_BAD_REQUEST)


class AnbarDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Anbar.objects.all()
    serializer_class = AnbarSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = AnbarFilter
    permission_classes = [muqavile_permissions.AnbarPermissions]

    def destroy(self, request, *args, **kwargs):
        anbar = self.get_object()
        anbar.is_active = False
        anbar.save()
        return Response({"detail": "Anbar qeyri-atkiv edildi"}, status=status.HTTP_200_OK)

# ********************************** anbar put delete post get **********************************
class AnbarQeydlerListCreateAPIView(generics.ListCreateAPIView):
    queryset = AnbarQeydler.objects.all()
    serializer_class = AnbarQeydlerSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = AnbarQeydlerFilter
    permission_classes = [muqavile_permissions.AnbarQeydlerPermissions]

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            queryset = AnbarQeydler.objects.all()
        elif request.user.shirket is not None:
            if request.user.ofis is not None:
                queryset = AnbarQeydler.objects.filter(anbar__shirket=request.user.shirket, anbar__ofis=request.user.ofis)
            queryset = AnbarQeydler.objects.filter(anbar__shirket=request.user.shirket)
        else:
            queryset = AnbarQeydler.objects.all()
        
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
        if serializer.is_valid():
            serializer.save(gonderen_user=user)
            return Response({"detail": "Sorğu göndərildi"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"detail": "Məlumatları doğru daxil edin."}, status=status.HTTP_400_BAD_REQUEST)


class AnbarQeydlerDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AnbarQeydler.objects.all()
    serializer_class = AnbarQeydlerSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = AnbarQeydlerFilter
    permission_classes = [muqavile_permissions.AnbarQeydlerPermissions]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "Sorğu yeniləndi"}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Məlumatları doğru daxil edin."}, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"detail": "Əməliyyat yerinə yetirildi"}, status=status.HTTP_204_NO_CONTENT)

# ********************************** emeliyyat put delete post get **********************************
class EmeliyyatListCreateAPIView(generics.ListCreateAPIView):
    queryset = Emeliyyat.objects.all()
    serializer_class = EmeliyyatSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = EmeliyyatFilter
    permission_classes = [muqavile_permissions.EmeliyyatPermissions]

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            queryset = Emeliyyat.objects.all()
        elif request.user.shirket is not None:
            if request.user.ofis is not None:
                queryset = Emeliyyat.objects.filter(gonderen__shirket=request.user.shirket, gonderen__ofis=request.user.ofis, qebul_eden__shirket=request.user.shirket, qebul_eden__ofis=request.user.ofis)
            queryset = Emeliyyat.objects.filter(gonderen__shirket=request.user.shirket, qebul_eden__shirket=request.user.shirket)
        else:
            queryset = Emeliyyat.objects.all()
        
        queryset = self.filter_queryset(queryset)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        return anbar_emeliyyat_utils.emeliyyat_create(self, request, *args, **kwargs)

class EmeliyyatDetailAPIView(generics.RetrieveUpdateAPIView):
    queryset = Emeliyyat.objects.all()
    serializer_class = EmeliyyatSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = EmeliyyatFilter
    permission_classes = [muqavile_permissions.EmeliyyatPermissions]

    def update(self, request, *args, **kwargs):
        return anbar_emeliyyat_utils.emeliyyat_create(self, request, *args, **kwargs)

# ********************************** stok put delete post get **********************************

class StokListCreateAPIView(generics.ListCreateAPIView):
    queryset = Stok.objects.all()
    serializer_class = StokSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = StokFilter
    permission_classes = [muqavile_permissions.StokPermissions]

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            queryset = Stok.objects.all()
        elif request.user.shirket is not None:
            if request.user.ofis is not None:
                queryset = Stok.objects.filter(anbar__shirket=request.user.shirket, anbar__ofis=request.user.ofis)
            queryset = Stok.objects.filter(anbar__shirket=request.user.shirket)
        else:
            queryset = Stok.objects.all()
        
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
            anbar = serializer.validated_data.get("anbar")
            mehsul = serializer.validated_data.get("mehsul")
            stok = Stok.objects.filter(anbar=anbar, mehsul=mehsul)
            if len(stok)>0:
                return Response({"detail": "Bu adlı stok artıq var. Yenisini əlavə edə bilməzsiniz"}, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response({"detail": "Stok əlavə edildi"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"detail": "Məlumatları doğru daxil edin"}, status=status.HTTP_400_BAD_REQUEST)


class StokDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Stok.objects.all()
    serializer_class = StokSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = StokFilter
    permission_classes = [muqavile_permissions.StokPermissions]

    def update(self, request, *args, **kwargs):
        return stok_utils.stok_update(self, request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"detail": "Əməliyyat yerinə yetirildi"}, status=status.HTTP_204_NO_CONTENT)
