import datetime
import django
from django.contrib.auth import user_logged_in
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework import generics

from restAPI.v1.account.serializers import (
    BolgeSerializer,
    GroupReadSerializer,
    RegisterSerializer,
    ResetPasswordSerializer,
    UserSerializer,
    MusteriSerializer,
    MusteriQeydlerSerializer,
    IsciSatisSayiSerializer,
    IsciStatusSerializer,
    PermissionSerializer,
    GroupSerializer,
    ChangePasswordSerializer
)

from account.models import (
    Bolge,
    IsciSatisSayi,
    MusteriQeydler, 
    User, 
    Musteri,
    IsciStatus
)

from django.contrib.auth.models import Permission, Group

from rest_framework_simplejwt.views import TokenObtainPairView

from restAPI.v1.account import utils

from restAPI.v1.account import permissions as account_permissions

from django_filters.rest_framework import DjangoFilterBackend

from restAPI.v1.account.filters import (
    BolgeFilter,
    IsciStatusFilter,
    MusteriFilter,
    MusteriQeydlerFilter,
    UserFilter,
    PermissionFilter,
    GroupFilter
)

import traceback

from company.models import VezifePermission
from rest_framework.permissions import IsAuthenticated  

# ********************************** Password change **********************************
class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """
    # class Meta:
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ********************************** Password change **********************************
class ResetPasswordView(generics.UpdateAPIView):
    """
    An endpoint for resetting password.
    """
    # class Meta:
    serializer_class = ResetPasswordSerializer
    model = User
    permission_classes = [account_permissions.PasswordResetPermissions]

    
    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            username = serializer.data.get("username")
            user = User.objects.filter(username = username).first()
            # Check old password
            if not user:
                return Response({"detail": "Bu username-ə uyğun istifadəçi tapılmadı"}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            user.set_password(serializer.data.get("new_password"))
            user.save()
            return Response({"detail": f"İstifadəçi adı {user.username} olan istifadçinin şifrəsi yeniləndi"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ********************************** permission model get post put delete **********************************
class PermissionListApi(generics.ListAPIView):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = PermissionFilter
    permission_classes = [account_permissions.PermissionModelPermissions]

# ********************************** permission group model get post put delete **********************************
class GroupListApi(generics.ListAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupReadSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = GroupFilter
    permission_classes = [account_permissions.GroupPermissions]

class GroupCreateApi(generics.CreateAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [account_permissions.GroupPermissions]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"detail" : f"Permission group əlavə olundu"}, status=status.HTTP_201_CREATED)

class GroupDetailApi(generics.RetrieveUpdateDestroyAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = GroupFilter
    permission_classes = [account_permissions.GroupPermissions]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"detail" : f"Permission group yeniləndi"}, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"detail": "Permission Group silindi"}, status=status.HTTP_204_NO_CONTENT)

# ********************************** user get post put delete **********************************


class RegisterApi(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if(serializer.is_valid()):
            komanda = serializer.validated_data.get('komanda')
            if komanda is not None:
                komanda = komanda
            else:
                komanda = None

            # standart_status = IsciStatus.objects.get(status_adi="STANDART")
            # if serializer.validated_data.get('isci_status') == None:
            #     isci_status = standart_status
            # else:
            #     isci_status=serializer.validated_data.get('isci_status')
                
            if serializer.validated_data.get('maas') == None:
                maas = 0
            elif serializer.validated_data.get('maas') is not None:
                maas = serializer.validated_data.get('maas')
            
            user_permissions=serializer.validated_data.get('user_permissions')

            serializer.save(
                komanda=komanda, user_permissions=user_permissions, maas=maas
            )
            return Response({"detail": "İşçi qeydiyyatdan keçirildi"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"detail": f"{serializer.errors}"}, status=status.HTTP_400_BAD_REQUEST)
            # return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = UserFilter
    permission_classes = [account_permissions.UserPermissions]

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            queryset = User.objects.all()
        elif request.user.shirket is not None:
            if request.user.ofis is not None:
                queryset = User.objects.filter(shirket=request.user.shirket, ofis=request.user.ofis)
            queryset = User.objects.filter(shirket=request.user.shirket)
        else:
            queryset = User.objects.all()
        
        queryset = self.filter_queryset(queryset)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = UserFilter
    permission_classes = [account_permissions.UserPermissions]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response({"detail" : "İşçi məlumatları yeniləndi"}, status=status.HTTP_200_OK)
        else:
            return Response({"detail" : "Məlumatları doğru daxil edin"}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        user = self.get_object()
        user.is_active = False
        user.ishden_cixma_tarixi = datetime.date.today()
        user.save()
        return Response({"detail": "İşçi qeyri-atkiv edildi"}, status=status.HTTP_200_OK)


class Login(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        data = super().post(request, *args, **kwargs)

        data = data.data

        acces_token = utils.jwt_decode_handler(data.get("access"))

        if not User.objects.filter(id=acces_token.get("user_id")).last():
            return Response({"error": True, "message": "No such a user"}, status=status.HTTP_404_NOT_FOUND)

        user = User.objects.filter(id=acces_token.get("user_id")).last()
        user_logged_in.send(sender=type(user), request=request, user=user)

        user_details = UserSerializer(user)

        data["user_details"] = user_details.data
        return Response(data)


# ********************************** musteri get post put delete **********************************
class MusteriListCreateAPIView(generics.ListCreateAPIView):
    queryset = Musteri.objects.all()
    serializer_class = MusteriSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = MusteriFilter
    permission_classes = [account_permissions.MusteriPermissions]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if (serializer.is_valid()):
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)


class MusteriDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Musteri.objects.all()
    serializer_class = MusteriSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = MusteriFilter
    permission_classes = [account_permissions.MusteriPermissions]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        musteri = self.get_object()
        musteri.is_active = False
        musteri.save()
        return Response({"detail": "Müştəri qeyri-atkiv edildi"}, status=status.HTTP_200_OK)

# ********************************** musteriqeydlerin put delete post get **********************************

class MusteriQeydlerListCreateAPIView(generics.ListCreateAPIView):
    queryset = MusteriQeydler.objects.all()
    serializer_class = MusteriQeydlerSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = MusteriQeydlerFilter
    permission_classes = [account_permissions.MusteriQeydlerPermissions]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({"detail": "Qeyd əlavə olundu"}, status=status.HTTP_201_CREATED, headers=headers)


class MusteriQeydlerDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MusteriQeydler.objects.all()
    serializer_class = MusteriQeydlerSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = MusteriQeydlerFilter
    permission_classes = [account_permissions.MusteriQeydlerPermissions]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response({"detail": "Əməliyyat yerinə yetirildi"}, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"detail": "Əməliyyat yerinə yetirildi"}, status=status.HTTP_204_NO_CONTENT)



# ********************************** bolge put delete post get **********************************

class BolgeListCreateAPIView(generics.ListCreateAPIView):
    queryset = Bolge.objects.all()
    serializer_class = BolgeSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = BolgeFilter
    permission_classes = [account_permissions.BolgePermissions]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        bolge = serializer.validated_data.get("bolge_adi")
        bolgeler = Bolge.objects.filter(bolge_adi=bolge)
        if len(bolgeler)>0:
            return Response({"detail": "Eyni adlı bölgəni 2 dəfə əlavə etmək olmaz!"}, status=status.HTTP_400_BAD_REQUEST)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({"detail": "Bölgə əlavə olundu"}, status=status.HTTP_201_CREATED, headers=headers)


class BolgeDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Bolge.objects.all()
    serializer_class = BolgeSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = BolgeFilter
    permission_classes = [account_permissions.BolgePermissions]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response({"detail": "Əməliyyat yerinə yetirildi"}, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"detail": "Əməliyyat yerinə yetirildi"}, status=status.HTTP_204_NO_CONTENT)


# ********************************** isci satis sayi put delete post get **********************************

class IsciSatisSayiListCreateAPIView(generics.ListCreateAPIView):
    queryset = IsciSatisSayi.objects.all()
    serializer_class = IsciSatisSayiSerializer
    permission_classes = [account_permissions.IsciSatisSayiPermissions]


class IsciSatisSayiDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = IsciSatisSayi.objects.all()
    serializer_class = IsciSatisSayiSerializer
    permission_classes = [account_permissions.IsciSatisSayiPermissions]


# ********************************** status put delete post get **********************************

class IsciStatusListCreateAPIView(generics.ListCreateAPIView):
    queryset = IsciStatus.objects.all()
    serializer_class = IsciStatusSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = IsciStatusFilter
    permission_classes = [account_permissions.IsciStatusPermissions]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        status_adi = serializer.validated_data.get("status_adi")
        statuslar = IsciStatus.objects.filter(status_adi=status_adi.upper())
        if len(statuslar)>0:
            return Response({"detail": "Eyni adlı statusu 2 dəfə əlavə etmək olmaz!"}, status=status.HTTP_400_BAD_REQUEST)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({"detail": "Status əlavə olundu"}, status=status.HTTP_201_CREATED, headers=headers)


class IsciStatusDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = IsciStatus.objects.all()
    serializer_class = IsciStatusSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = IsciStatusFilter
    permission_classes = [account_permissions.IsciStatusPermissions]

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

        return Response({"detail": "Status məlumatları yeniləndi"})

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"detail" : "İşçi statusu silindi"}, status=status.HTTP_204_NO_CONTENT)
