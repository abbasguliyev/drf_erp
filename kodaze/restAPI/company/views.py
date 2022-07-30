from rest_framework import status, generics
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.response import Response

from restAPI.company.serializers import (
    ShirketSerializer,
    KomandaSerializer,
    OfisSerializer,
    ShobeSerializer,
    VezifePermissionSerializer,
    VezifelerSerializer,
    HoldingSerializer,
)

from account.models import User

from company.models import (
    Holding,
    Shirket,
    Ofis,
    Komanda,
    Shobe,
    VezifePermission,
    Vezifeler
)


from restAPI.company.filters import (
    KomandaFilter,
    OfisFilter,
    ShirketFilter,
    ShobeFilter,
    VezifeFilter,
    VezifePermissionFilter
)

from restAPI.company import permissions as company_permissions
from django.contrib.auth.models import Group

# ********************************** komanda get post put delete **********************************


class KomandaListCreateAPIView(generics.ListCreateAPIView):
    queryset = Komanda.objects.all()
    serializer_class = KomandaSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = KomandaFilter
    permission_classes = [company_permissions.KomandaPermissions]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        komanda_adi = serializer.validated_data.get("komanda_adi")
        komandalar = Komanda.objects.filter(komanda_adi=komanda_adi.upper())
        if len(komandalar) > 0:
            return Response({"detail": "Bu adla komanda artıq qeydiyyatdan keçirilib"}, status=status.HTTP_400_BAD_REQUEST)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({"detail": "Komanda əlavə edildi"}, status=status.HTTP_201_CREATED, headers=headers)


class KomandaDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Komanda.objects.all()
    serializer_class = KomandaSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = KomandaFilter
    permission_classes = [company_permissions.KomandaPermissions]

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response({"detail": "Komanda məlumatları yeniləndi"})

    def destroy(self, request, *args, **kwargs):
        komanda = self.get_object()
        komanda.is_active = False
        komanda.save()
        return Response({"detail": "Komanda qeyri-atkiv edildi"}, status=status.HTTP_200_OK)



# ********************************** ofisler put delete post get **********************************


class OfisListCreateAPIView(generics.ListCreateAPIView):
    queryset = Ofis.objects.all()
    serializer_class = OfisSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = OfisFilter
    permission_classes = [company_permissions.OfisPermissions]

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            queryset = Ofis.objects.all()
        elif request.user.shirket is not None:
            if request.user.ofis is not None:
                queryset = Ofis.objects.filter(shirket=request.user.shirket, id=request.user.ofis.id)
            queryset = Ofis.objects.filter(shirket=request.user.shirket)
        else:
            queryset = Ofis.objects.all()
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
        return Response({"detail": "Ofis əlavə olundu"}, status=status.HTTP_201_CREATED, headers=headers)


class OfisDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ofis.objects.all()
    serializer_class = OfisSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = OfisFilter
    permission_classes = [company_permissions.OfisPermissions]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"detail":"Ofis məlumatları yeniləndi"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"detail":"Məlumatları doğru daxil etdiyinizdən əmin olun"}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return Response({"detail":"Ofis deaktiv edildi"}, status=status.HTTP_200_OK)

# ********************************** vezifeler put delete post get **********************************


class VezifelerListCreateAPIView(generics.ListCreateAPIView):
    queryset = Vezifeler.objects.all()
    serializer_class = VezifelerSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = VezifeFilter
    permission_classes = [company_permissions.VezifelerPermissions]

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            queryset = Vezifeler.objects.all()
        elif request.user.shirket is not None:
            queryset = Vezifeler.objects.filter(shirket=request.user.shirket)
        else:
            queryset = Vezifeler.objects.all()
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
        vezife_adi = serializer.validated_data.get("vezife_adi")
        shirket = serializer.validated_data.get("shirket")
        vezife_db = Vezifeler.objects.filter(vezife_adi=vezife_adi.upper(), shirket=shirket)
        if len(vezife_db) > 0:
            return Response({"detail":"Bu ad və şirkətə uyğun vəzifə artıq qeydiyyatdan keçirilib"}, status=status.HTTP_400_BAD_REQUEST)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({"detail": "Vəzifə əlavə olundu"}, status=status.HTTP_201_CREATED, headers=headers)



class VezifelerDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vezifeler.objects.all()
    serializer_class = VezifelerSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = VezifeFilter
    permission_classes = [company_permissions.VezifelerPermissions]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"detail":"Vəzifə məlumatları yeniləndi"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"detail":"Məlumatları doğru daxil etdiyinizdən əmin olun"}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return Response({"detail":"Vəzifə deaktiv edildi"}, status=status.HTTP_200_OK)

# ********************************** shirket put delete post get **********************************
class ShirketListCreateAPIView(generics.ListCreateAPIView):
    queryset = Shirket.objects.all()
    serializer_class = ShirketSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ShirketFilter
    permission_classes = [company_permissions.ShirketPermissions]

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            queryset = Shirket.objects.all()
        elif request.user.shirket is not None:
            queryset = Shirket.objects.filter(id=request.user.shirket.id)
        else:
            queryset = Shirket.objects.all()
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
        return Response({"detail": "Şirkət əlavə olundu"}, status=status.HTTP_201_CREATED, headers=headers)


class ShirketDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Shirket.objects.all()
    serializer_class = ShirketSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ShirketFilter
    permission_classes = [company_permissions.ShirketPermissions]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"detail":"Şirkət məlumatları yeniləndi"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"detail":"Məlumatları doğru daxil etdiyinizdən əmin olun"}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return Response({"detail":"Şirkət deaktiv edildi"}, status=status.HTTP_200_OK)

# ********************************** shobe put delete post get **********************************


class ShobeListCreateAPIView(generics.ListCreateAPIView):
    queryset = Shobe.objects.all()
    serializer_class = ShobeSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ShobeFilter
    permission_classes = [company_permissions.ShobePermissions]

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            queryset = Shobe.objects.all()
        elif request.user.shirket is not None:
            if request.user.ofis is not None:
                queryset = Shobe.objects.filter(ofis__shirket=request.user.shirket, ofis=request.user.ofis)
            queryset = Shobe.objects.filter(ofis__shirket=request.user.shirket)
        else:
            queryset = Shobe.objects.all()
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
        return Response({"detail": "Şöbə əlavə olundu"}, status=status.HTTP_201_CREATED, headers=headers)

class ShobeDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Shobe.objects.all()
    serializer_class = ShobeSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ShobeFilter
    permission_classes = [company_permissions.ShobePermissions]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"detail":"Şöbə məlumatları yeniləndi"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"detail":"Məlumatları doğru daxil etdiyinizdən əmin olun"}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return Response({"detail":"Şöbə deaktiv edildi"}, status=status.HTTP_200_OK)


# ********************************** holding put delete post get **********************************

class HoldingListCreateAPIView(generics.ListCreateAPIView):
    queryset = Holding.objects.all()
    serializer_class = HoldingSerializer
    permission_classes = [company_permissions.HoldingPermissions]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({"detail": "Holding əlavə olundu"}, status=status.HTTP_201_CREATED, headers=headers)


class HoldingDetailAPIView(generics.RetrieveUpdateAPIView):
    queryset = Holding.objects.all()
    serializer_class = HoldingSerializer
    permission_classes = [company_permissions.HoldingPermissions]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"detail":"Holding məlumatları yeniləndi"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"detail":"Məlumatları doğru daxil etdiyinizdən əmin olun"}, status=status.HTTP_400_BAD_REQUEST)

# ********************************** VezifePermission put delete post get **********************************

class VezifePermissionListCreateAPIView(generics.ListCreateAPIView):
    queryset = VezifePermission.objects.all()
    serializer_class = VezifePermissionSerializer
    permission_classes = [company_permissions.VezifePermissionPermissions]
    filter_backends = [DjangoFilterBackend]
    filterset_class = VezifePermissionFilter

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            queryset = VezifePermission.objects.all()
        elif request.user.shirket is not None:
            queryset = VezifePermission.objects.filter(vezife__shirket=request.user.shirket)
        else:
            queryset = VezifePermission.objects.all()
        queryset = self.filter_queryset(queryset)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        vezife_id = request.data.get("vezife_id")
        vezife =Vezifeler.objects.get(pk=vezife_id)
        permission_group_id = request.data.get("permission_group_id")
        permission_group = Group.objects.get(pk=permission_group_id)
        users = User.objects.filter(vezife=vezife)
        if permission_group is not None or permission_group == list():
            for user in users:
                user.groups.add(permission_group)

        VezifePermission.objects.create(
            vezife = vezife,
            permission_group=permission_group
        ).save()
        return Response({"detail" : f"{vezife} üçün permission təyin olundu"}, status=status.HTTP_201_CREATED)
        

class VezifePermissionDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = VezifePermission.objects.all()
    serializer_class = VezifePermissionSerializer
    permission_classes = [company_permissions.VezifePermissionPermissions]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            vezife = instance.vezife
            users = User.objects.filter(vezife=vezife)
            permission_group = instance.permission_group
            request_permission_group = serializer.validated_data.get("permission_group")

            if request_permission_group is not None or permission_group == list():
                for user in users:
                    user.groups.add(request_permission_group)
                    user.save()

            serializer.save()
            return Response({"detail" : f"{vezife} üçün permission yeniləndi"}, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        permission_group = instance.permission_group
        vezife = instance.vezife
        users = User.objects.filter(vezife=vezife)

        for user in users:
            user.groups.remove(permission_group)
            user.save()
        instance.delete()
        return Response({"detail" : f"Vəzifə permission silindi"}, status=status.HTTP_200_OK)
