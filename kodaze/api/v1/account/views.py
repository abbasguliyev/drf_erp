import datetime
import django
from django.contrib.auth import user_logged_in
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.views import APIView

from api.v1.account.serializers import (
    RegionSerializer,
    RegisterSerializer,
    ResetPasswordSerializer,
    UserSerializer,
    CustomerSerializer,
    CustomerNoteSerializer,
    EmployeeStatusSerializer,
    PermissionSerializer,
    GroupSerializer,
    ChangePasswordSerializer
)

from account.models import (
    Region,
    CustomerNote, 
    User, 
    Customer,
    EmployeeStatus
)

from django.contrib.auth.models import Permission, Group

from rest_framework_simplejwt.views import TokenObtainPairView

from api.v1.account import utils

from api.v1.account import permissions as account_permissions

from django_filters.rest_framework import DjangoFilterBackend

from api.v1.account.filters import (
    RegionFilter,
    EmployeeStatusFilter,
    CustomerFilter,
    CustomerNoteFilter,
    UserFilter,
    PermissionFilter,
    GroupFilter
)

import traceback

from company.models import PermissionForPosition
from rest_framework.permissions import IsAuthenticated  
import json
import os
from core.settings import BASE_DIR

from api.v1.account.services import all_region_create, create_customer, create_employee_status, create_user, update_user, region_create


from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie

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
                'detail': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ********************************** Password change **********************************
class ResetPasswordView(generics.UpdateAPIView):
    """
    An endpoint for resetting password.
    """
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
    serializer_class = GroupSerializer
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
    queryset = User.objects.select_related(
                'holding', 'company', 'office', 'section', 'position', 'team', 'employee_status', 'commission', 'department'
            ).prefetch_related('user_permissions', 'groups').all()
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if(serializer.is_valid()):
            create_user(**serializer.validated_data)
            return Response({"detail": "İşçi qeydiyyatdan keçirildi"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"detail": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class UserList(generics.ListAPIView):
    queryset = User.objects.select_related(
                'holding', 'company', 'office', 'section', 'position', 'team', 'employee_status', 'department'
            ).prefetch_related('user_permissions', 'groups').all()
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = UserFilter
    permission_classes = [account_permissions.UserPermissions]
    
    # @method_decorator(vary_on_cookie)
    # @method_decorator(cache_page(60*60, key_prefix="users"))
    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            queryset = self.queryset
        elif request.user.company is not None:
            if request.user.office is not None:
                queryset = self.queryset.filter(company=request.user.company, office=request.user.office)
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


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.select_related(
                'holding', 'company', 'office', 'section', 'position', 'team', 'employee_status', 'department'
            ).prefetch_related('user_permissions', 'groups').all()
    serializer_class = UserSerializer
    permission_classes = [account_permissions.UserPermissions]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        
        if serializer.is_valid():
            update_user(instance.id, **serializer.validated_data)
            return Response({"detail" : "İşçi məlumatları yeniləndi"}, status=status.HTTP_200_OK)
        else:
            return Response({"detail" : "Məlumatları doğru daxil edin"}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        user = self.get_object()
        user.is_active = False
        user.dismissal_date = datetime.date.today()
        user.save()
        return Response({"detail": "İşçi qeyri-atkiv edildi"}, status=status.HTTP_200_OK)


class Login(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        data = super().post(request, *args, **kwargs)

        data = data.data

        acces_token = utils.jwt_decode_handler(data.get("access"))

        if not User.objects.select_related(
                'company', 'office', 'section', 'position', 'team', 'employee_status', 'department'
            ).prefetch_related('user_permissions', 'groups').filter(id=acces_token.get("user_id")).last():
            return Response({"error": True, "detail": "No such a user"}, status=status.HTTP_404_NOT_FOUND)

        user = User.objects.select_related(
                'company', 'office', 'section', 'position', 'team', 'employee_status', 'department'
            ).prefetch_related('user_permissions', 'groups').filter(id=acces_token.get("user_id")).last()
        user_logged_in.send(sender=type(user), request=request, user=user)

        user_details = UserSerializer(user)

        data["user_details"] = user_details.data
        return Response(data)


# ********************************** customer get post put delete **********************************
class CustomerListCreateAPIView(generics.ListCreateAPIView):
    queryset = Customer.objects.select_related('region').all()
    serializer_class = CustomerSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CustomerFilter
    permission_classes = [account_permissions.CustomerPermissions]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if (serializer.is_valid()):
            create_customer(**serializer.validated_data)
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({"detail" : serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class CustomerDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Customer.objects.select_related('region').all()
    serializer_class = CustomerSerializer
    permission_classes = [account_permissions.CustomerPermissions]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        customer = self.get_object()
        customer.is_active = False
        customer.save()
        return Response({"detail": "Müştəri qeyri-atkiv edildi"}, status=status.HTTP_200_OK)

# ********************************** customer note put delete post get **********************************

class CustomerNoteListCreateAPIView(generics.ListCreateAPIView):
    queryset = CustomerNote.objects.select_related('customer').all()
    serializer_class = CustomerNoteSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CustomerNoteFilter
    permission_classes = [account_permissions.CustomerNotePermissions]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({"detail": "Qeyd əlavə olundu"}, status=status.HTTP_201_CREATED, headers=headers)


class CustomerNoteDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomerNote.objects.select_related('customer').all()
    serializer_class = CustomerNoteSerializer
    permission_classes = [account_permissions.CustomerNotePermissions]

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



# ********************************** region put delete post get **********************************

class RegionListCreateAPIView(generics.ListCreateAPIView):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = RegionFilter
    permission_classes = [account_permissions.RegionPermissions]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            region_create(**serializer.validated_data)
            return Response({"detail": "Bölgə əlavə olundu"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"detail": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
class AllRegionCreate(APIView):
    def post(self, request, *args, **kwargs):
        try:
            all_region_create()
            return Response({"detail": "Bölgələr əlavə olundu"}, status=status.HTTP_201_CREATED)
        except:
            return Response({"detail": "Xəta baş verdi"}, status=status.HTTP_404_NOT_FOUND)

class RegionDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = RegionFilter
    permission_classes = [account_permissions.RegionPermissions]

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



# ********************************** status put delete post get **********************************

class EmployeeStatusListCreateAPIView(generics.ListCreateAPIView):
    queryset = EmployeeStatus.objects.all()
    serializer_class = EmployeeStatusSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = EmployeeStatusFilter
    permission_classes = [account_permissions.EmployeeStatusPermissions]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            create_employee_status(**serializer.validated_data)
            return Response({"detail": "Status əlavə olundu"}, status=status.HTTP_201_CREATED)
        return Response({"detail": "Məlumatları doğru daxil edin"}, status=status.HTTP_400_BAD_REQUEST)


class EmployeeStatusDetailAPIView(generics.RetrieveDestroyAPIView):
    queryset = EmployeeStatus.objects.all()
    serializer_class = EmployeeStatusSerializer
    permission_classes = [account_permissions.EmployeeStatusPermissions]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"detail" : "İşçi statusu silindi"}, status=status.HTTP_204_NO_CONTENT)