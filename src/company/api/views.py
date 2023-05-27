from django.contrib.auth.models import Group
from rest_framework import status, generics, permissions
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend


from company.api.serializers import (
    AppLogoSerializer,
    CompanySerializer,
    TeamSerializer,
    OfficeSerializer,
    SectionSerializer,
    PermissionForPositionSerializer,
    PositionSerializer,
    HoldingSerializer,
    DepartmentSerializer
)

from company.models import (
    AppLogo,
    Team,
    PermissionForPosition,
)


from company.api.filters import (
    TeamFilter,
    OfficeFilter,
    CompanyFilter,
    SectionFilter,
    PositionFilter,
    PermissionForPositionFilter,
    DepartmentFilter
)

from company.tasks import deactive_employees_of_a_specific_company
from company.api import permissions as company_permissions
from company.api.selectors import holding_list, company_list, office_list, section_list, department_list, team_list, position_list
from account.api.selectors import user_list
from warehouse.api.selectors import warehouse_list
from .services import company_create, holding_create, department_create, office_create, office_update, position_create, section_create


# ********************************** holding endpoints **********************************

class HoldingListCreateAPIView(generics.ListCreateAPIView):
    queryset = holding_list()
    serializer_class = HoldingSerializer
    permission_classes = [company_permissions.HoldingPermissions]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        holding_create(**serializer.validated_data)
        return Response({"detail": "Holding əlavə olundu"}, status=status.HTTP_201_CREATED)


class HoldingDetailAPIView(generics.RetrieveUpdateAPIView):
    queryset = holding_list()
    serializer_class = HoldingSerializer
    permission_classes = [company_permissions.HoldingPermissions]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "Holding məlumatları yeniləndi"}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Məlumatları doğru daxil etdiyinizdən əmin olun"}, status=status.HTTP_400_BAD_REQUEST)

# ********************************** company endpoints **********************************

class CompanyListCreateAPIView(generics.ListCreateAPIView):
    queryset = company_list()
    serializer_class = CompanySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CompanyFilter
    permission_classes = [company_permissions.CompanyPermissions]

    def get(self, request, *args, **kwargs):
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
        if serializer.is_valid(raise_exception=True):
            company_create(**serializer.validated_data)
            return Response({"detail": "Şirkət əlavə olundu"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"detail": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class CompanyDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = company_list()
    serializer_class = CompanySerializer
    permission_classes = [company_permissions.CompanyPermissions]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "Şirkət məlumatları yeniləndi"}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Məlumatları doğru daxil etdiyinizdən əmin olun"}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        deactive_employees_of_a_specific_company.delay(company_id = instance.id)
        return Response({"detail": "Şirkət deaktiv edildi"}, status=status.HTTP_200_OK)

# ********************************** department endpoints **********************************

class DepartmentListCreateAPIView(generics.ListCreateAPIView):
    queryset = department_list()
    serializer_class = DepartmentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = DepartmentFilter
    permission_classes = [company_permissions.DepartmentPermissions]

    def get(self, request, *args, **kwargs):
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
        if serializer.is_valid(raise_exception=True):
            department_create(**serializer.validated_data)
            return Response({"detail": "Departament əlavə olundu"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"detail": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class DepartmentDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = department_list()
    serializer_class = DepartmentSerializer
    permission_classes = [company_permissions.DepartmentPermissions]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "Departament məlumatları yeniləndi"}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Məlumatları doğru daxil etdiyinizdən əmin olun"}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return Response({"detail": "Departament deaktiv edildi"}, status=status.HTTP_200_OK)

# ********************************** officeler endpoints **********************************

class OfficeListCreateAPIView(generics.ListCreateAPIView):
    queryset = office_list()
    serializer_class = OfficeSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = OfficeFilter
    permission_classes = [company_permissions.OfficePermissions]

    def get(self, request, *args, **kwargs):
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
        if serializer.is_valid(raise_exception=True):
            office_create(**serializer.validated_data)
            return Response({"detail": "Ofis əlavə olundu"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"detail": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class OfficeDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = office_list()
    serializer_class = OfficeSerializer
    permission_classes = [company_permissions.OfficePermissions]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            office_update(instance=instance, **serializer.validated_data)
            return Response({"detail": "Ofis məlumatları yeniləndi"}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Məlumatları doğru daxil etdiyinizdən əmin olun"}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        warehouses = warehouse_list().filter(office=instance)
        for warehouse in warehouses:
            warehouse.is_active = False
            warehouse.save()
        return Response({"detail": "Ofis deaktiv edildi"}, status=status.HTTP_200_OK)

# ********************************** section endpoints **********************************

class SectionListCreateAPIView(generics.ListCreateAPIView):
    queryset = section_list()
    serializer_class = SectionSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = SectionFilter
    permission_classes = [company_permissions.SectionPermissions]

    def get(self, request, *args, **kwargs):
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
        if serializer.is_valid(raise_exception=True):
            section_create(**serializer.validated_data)
            return Response({"detail": "Şöbə əlavə olundu"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"detail": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class SectionDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = section_list()
    serializer_class = SectionSerializer
    permission_classes = [company_permissions.SectionPermissions]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "Şöbə məlumatları yeniləndi"}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Məlumatları doğru daxil etdiyinizdən əmin olun"}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return Response({"detail": "Şöbə deaktiv edildi"}, status=status.HTTP_200_OK)

# ********************************** team endpoints **********************************

class TeamListCreateAPIView(generics.ListCreateAPIView):
    queryset = team_list()
    serializer_class = TeamSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = TeamFilter
    permission_classes = [company_permissions.TeamPermissions]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        name = serializer.validated_data.get("name")
        teamlar = Team.objects.filter(name=name.upper())
        if len(teamlar) > 0:
            return Response({"detail": "Bu adla komanda artıq qeydiyyatdan keçirilib"}, status=status.HTTP_400_BAD_REQUEST)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({"detail": "Komanda əlavə edildi"}, status=status.HTTP_201_CREATED, headers=headers)


class TeamDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = team_list()
    serializer_class = TeamSerializer
    permission_classes = [company_permissions.TeamPermissions]

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response({"detail": "Komanda məlumatları yeniləndi"})

    def destroy(self, request, *args, **kwargs):
        team = self.get_object()
        team.is_active = False
        team.save()
        return Response({"detail": "Komanda qeyri-atkiv edildi"}, status=status.HTTP_200_OK)

# ********************************** position endpoints **********************************


class PositionListCreateAPIView(generics.ListCreateAPIView):
    queryset = position_list()
    serializer_class = PositionSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = PositionFilter
    permission_classes = [company_permissions.PositionPermissions]

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            position_create(**serializer.validated_data)
            return Response({"detail": "Vəzifə əlavə olundu"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"detail": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class PositionDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = position_list()
    serializer_class = PositionSerializer
    permission_classes = [company_permissions.PositionPermissions]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "Vəzifə məlumatları yeniləndi"}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Məlumatları doğru daxil etdiyinizdən əmin olun"}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return Response({"detail": "Vəzifə deaktiv edildi"}, status=status.HTTP_200_OK)

# ********************************** PermissionForPosition endpoints **********************************

class PermissionForPositionListCreateAPIView(generics.ListCreateAPIView):
    queryset = PermissionForPosition.objects.select_related('position', 'permission_group').all()
    serializer_class = PermissionForPositionSerializer
    permission_classes = [company_permissions.PermissionForPositionPermissions]
    filter_backends = [DjangoFilterBackend]
    filterset_class = PermissionForPositionFilter

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        position_id = request.data.get("position_id")
        position = position_list().filter(pk=position_id).last
        permission_group_id = request.data.get("permission_group_id")
        permission_group = Group.objects.get(pk=permission_group_id)
        users = user_list().filter(position= position)
        if permission_group is not None or permission_group == list():
            for user in users:
                user.groups.add(permission_group)

        PermissionForPosition.objects.create(
            position=position,
            permission_group=permission_group
        ).save()
        return Response({"detail": f"{position.name} üçün permission təyin olundu"}, status=status.HTTP_201_CREATED)


class PermissionForPositionDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PermissionForPosition.objects.select_related('position', 'permission_group').all()
    serializer_class = PermissionForPositionSerializer
    permission_classes = [company_permissions.PermissionForPositionPermissions]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=True)
        if serializer.is_valid():
            position = instance.position
            users = user_list().filter(position= position)
            permission_group = instance.permission_group
            request_permission_group = serializer.validated_data.get(
                "permission_group")

            if request_permission_group is not None or permission_group == list():
                for user in users:
                    user.groups.add(request_permission_group)
                    user.save()

            serializer.save()
            return Response({"detail": f"{position} üçün permission yeniləndi"}, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        permission_group = instance.permission_group
        position = instance.position
        users = user_list().filter(position= position)

        for user in users:
            user.groups.remove(permission_group)
            user.save()
        instance.delete()
        return Response({"detail": f"Vəzifə permission silindi"}, status=status.HTTP_200_OK)

# -------------------- AppLogo Views -------------------------
class AppLogoListCreateAPIView(generics.ListCreateAPIView):
    queryset = AppLogo.objects.all()
    serializer_class = AppLogoSerializer
    permission_classes = [company_permissions.AppLogoPermissions]

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return super().get_permissions()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        logo = request.data.get("logo")
        try:
            app_logo = AppLogo.objects.all()
            if len(app_logo) > 0:
                app_logo[0].logo = logo
                app_logo[0].save()
            else:
                app_logo = AppLogo.objects.create(logo=logo)
                app_logo.save()
            return Response({"detail": "Logo əlavə edildi"}, status=status.HTTP_201_CREATED)
        except:
            return Response({"detail": "Məlumatları doğru daxil edin!"}, status=status.HTTP_400_BAD_REQUEST)

class AppLogoDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AppLogo.objects.all()
    serializer_class = AppLogoSerializer
    permission_classes = [company_permissions.AppLogoPermissions]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "Logo yeniləndi"}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Məlumatları doğru daxil edin!"}, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"detail": "Logo silindi"}, status=status.HTTP_200_OK)