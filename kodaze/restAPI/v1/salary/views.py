from salary.models import (
    AdvancePayment,
    Manager1PrimNew,
    SalaryDeduction,
    Bonus,
    CreditorPrim,
    SalaryView,
    PaySalary, 
    OfficeLeaderPrim,
    Manager2Prim,
    GroupLeaderPrimNew
)
from restAPI.v1.salary.serializers import (
    AdvancePaymentSerializer, 
    BonusSerializer,
    Manager1PrimNewSerializer,
    SalaryDeductionSerializer,
    SalaryViewSerializer,
    Manager2PrimSerializer,
    PaySalarySerializer,
    OfficeLeaderPrimSerializer,
    GroupLeaderPrimNewSerializer,
    CreditorPrimSerializer,
)
from rest_framework import status, generics

from rest_framework.response import Response

from restAPI.v1.salary import utils as salary_utils

from restAPI.v1.salary import permissions as salary_permissions

from django_filters.rest_framework import DjangoFilterBackend

from restAPI.v1.salary.filters import (
    AdvancePaymentFilter,
    BonusFilter,
    Manager2PrimFilter,
    Manager1PrimNewFilter,
    SalaryDeductionFilter,
    SalaryViewFilter,
    PaySalaryFilter,
    OfficeLeaderPrimFilter,
    GroupLeaderPrimNewFilter
)

# ********************************** AdvancePayment get post put delete **********************************
class AdvancePaymentListCreateAPIView(generics.ListCreateAPIView):
    queryset = AdvancePayment.objects.all()
    serializer_class = AdvancePaymentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = AdvancePaymentFilter
    permission_classes = [salary_permissions.AdvancePaymentPermissions]

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            queryset = AdvancePayment.objects.all()
        elif request.user.company is not None:
            if request.user.office is not None:
                queryset = AdvancePayment.objects.filter(employee__company=request.user.company, employee__office=request.user.office)
            queryset = AdvancePayment.objects.filter(employee__company=request.user.company)
        else:
            queryset = AdvancePayment.objects.all()
        queryset = self.filter_queryset(queryset)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        return salary_utils.advancepayment_create(self, request, *args, **kwargs)

class AdvancePaymentDetailAPIView(generics.RetrieveUpdateAPIView):
    queryset = AdvancePayment.objects.all()
    serializer_class = AdvancePaymentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = AdvancePaymentFilter
    permission_classes = [salary_permissions.AdvancePaymentPermissions]

# ********************************** SalaryDeduction get post put delete **********************************
class SalaryDeductionListCreateAPIView(generics.ListCreateAPIView):
    queryset = SalaryDeduction.objects.all()
    serializer_class = SalaryDeductionSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = SalaryDeductionFilter
    permission_classes = [salary_permissions.SalaryDeductionPermissions]

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            queryset = SalaryDeduction.objects.all()
        elif request.user.company is not None:
            if request.user.office is not None:
                queryset = SalaryDeduction.objects.filter(employee__company=request.user.company, employee__office=request.user.office)
            queryset = SalaryDeduction.objects.filter(employee__company=request.user.company)
        else:
            queryset = SalaryDeduction.objects.all()
        queryset = self.filter_queryset(queryset)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        return salary_utils.salarydeduction_create(self, request, *args, **kwargs)


class SalaryDeductionDetailAPIView(generics.RetrieveUpdateAPIView):
    queryset = SalaryDeduction.objects.all()
    serializer_class = SalaryDeductionSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = SalaryDeductionFilter
    permission_classes = [salary_permissions.SalaryDeductionPermissions]

# ********************************** Bonus get post put delete **********************************
class BonusListCreateAPIView(generics.ListCreateAPIView):
    queryset = Bonus.objects.all()
    serializer_class = BonusSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = BonusFilter
    permission_classes = [salary_permissions.BonusPermissions]

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            queryset = Bonus.objects.all()
        elif request.user.company is not None:
            if request.user.office is not None:
                queryset = Bonus.objects.filter(employee__company=request.user.company, employee__office=request.user.office)
            queryset = Bonus.objects.filter(employee__company=request.user.company)
        else:
            queryset = Bonus.objects.all()
        queryset = self.filter_queryset(queryset)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        return salary_utils.bonus_create(self, request, *args, **kwargs)


class BonusDetailAPIView(generics.RetrieveUpdateAPIView):
    queryset = Bonus.objects.all()
    serializer_class = BonusSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = BonusFilter
    permission_classes = [salary_permissions.BonusPermissions]

# ********************************** Maas Ode get post put delete **********************************
class PaySalaryListCreateAPIView(generics.ListCreateAPIView):
    queryset = PaySalary.objects.all()
    serializer_class = PaySalarySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = PaySalaryFilter
    permission_classes = [salary_permissions.PaySalaryPermissions]

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            queryset = PaySalary.objects.all()
        elif request.user.company is not None:
            if request.user.office is not None:
                queryset = PaySalary.objects.filter(employee__company=request.user.company, employee__office=request.user.office)
            queryset = PaySalary.objects.filter(employee__company=request.user.company)
        else:
            queryset = PaySalary.objects.all()
        queryset = self.filter_queryset(queryset)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        return salary_utils.salary_ode_create(self, request, *args, **kwargs)


class PaySalaryDetailAPIView(generics.RetrieveUpdateAPIView):
    queryset = PaySalary.objects.all()
    serializer_class = PaySalarySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = PaySalaryFilter
    permission_classes = [salary_permissions.PaySalaryPermissions]

# ********************************** SalaryView get post put delete **********************************
class SalaryViewListCreateAPIView(generics.ListCreateAPIView):
    queryset = SalaryView.objects.all()
    serializer_class = SalaryViewSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = SalaryViewFilter
    permission_classes = [salary_permissions.SalaryViewPermissions]

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            queryset = SalaryView.objects.all()
        elif request.user.company is not None:
            if request.user.office is not None:
                queryset = SalaryView.objects.filter(employee__company=request.user.company, employee__office=request.user.office)
            queryset = SalaryView.objects.filter(employee__company=request.user.company)
        else:
            queryset = SalaryView.objects.all()
        queryset = self.filter_queryset(queryset)
    
        sale_quantity = 0
        umumi_advancepayment = 0
        umumi_bonus = 0
        umumi_salarydeduction = 0

        for q in queryset:
            sale_quantity += q.sale_quantity

            month = q.date.month

            advancepayment = AdvancePayment.objects.filter(employee = q.employee, date__month=month)
            bonus = Bonus.objects.filter(employee = q.employee, date__month=month)
            salarydeduction = SalaryDeduction.objects.filter(employee = q.employee, date__month=month)

            for a in advancepayment:
                umumi_advancepayment += a.amount

            for b in bonus:
                umumi_bonus += b.amount

            for k in salarydeduction:
                umumi_salarydeduction += k.amount

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(
                {
                    'umumi_advancepayment': umumi_advancepayment, 
                    'umumi_bonus': umumi_bonus, 
                    'umumi_salarydeduction': umumi_salarydeduction,
                    'data':serializer.data
                }
            )

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class SalaryViewDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SalaryView.objects.all()
    serializer_class = SalaryViewSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = SalaryViewFilter
    permission_classes = [salary_permissions.SalaryViewPermissions]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"detail": "Əməliyyat yerinə yetirildi"}, status=status.HTTP_204_NO_CONTENT)

# ********************************** Office Leader Prim get post put delete **********************************
class OfficeLeaderPrimListCreateAPIView(generics.ListCreateAPIView):
    queryset = OfficeLeaderPrim.objects.all()
    serializer_class = OfficeLeaderPrimSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = OfficeLeaderPrimFilter
    permission_classes = [salary_permissions.OfficeLeaderPrimPermissions]

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            queryset = OfficeLeaderPrim.objects.all()
        elif request.user.company is not None:
            queryset = OfficeLeaderPrim.objects.filter(position__company=request.user.company)
        else:
            queryset = OfficeLeaderPrim.objects.all()
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
            prim_status = serializer.validated_data.get("prim_status")
            position = serializer.validated_data.get("position")
            prim = OfficeLeaderPrim.objects.filter(prim_status=prim_status, position=position)
            if len(prim)>0:
                return Response({"detail": "Bu status və vəzifəyə uyğun prim artıq əlavə olunub"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                serializer.save()
                return Response({"detail": "Prim əlavə edildi"})


class OfficeLeaderPrimDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = OfficeLeaderPrim.objects.all()
    serializer_class = OfficeLeaderPrimSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = OfficeLeaderPrimFilter
    permission_classes = [salary_permissions.OfficeLeaderPrimPermissions]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "Office Leader bonus yeniləndi"}, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"detail": "Əməliyyat yerinə yetirildi"}, status=status.HTTP_204_NO_CONTENT)

# ********************************** GroupLeader Prim New get post put delete **********************************
class GroupLeaderPrimNewListCreateAPIView(generics.ListCreateAPIView):
    queryset = GroupLeaderPrimNew.objects.all()
    serializer_class = GroupLeaderPrimNewSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = GroupLeaderPrimNewFilter
    permission_classes = [salary_permissions.GroupLeaderPrimNewPermissions]

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            queryset = GroupLeaderPrimNew.objects.all()
        elif request.user.company is not None:
            queryset = GroupLeaderPrimNew.objects.filter(position__company=request.user.company)
        else:
            queryset = GroupLeaderPrimNew.objects.all()
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
            prim_status = serializer.validated_data.get("prim_status")
            position = serializer.validated_data.get("position")
            prim = GroupLeaderPrimNew.objects.filter(prim_status=prim_status, position=position)
            if len(prim)>0:
                return Response({"detail": "Bu status və vəzifəyə uyğun prim artıq əlavə olunub"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                serializer.save()
                return Response({"detail": "Prim əlavə edildi"})


class GroupLeaderPrimNewDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = GroupLeaderPrimNew.objects.all()
    serializer_class = GroupLeaderPrimNewSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = GroupLeaderPrimNewFilter
    permission_classes = [salary_permissions.GroupLeaderPrimNewPermissions]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "Van Leader bonus yeniləndi"}, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"detail": "Əməliyyat yerinə yetirildi"}, status=status.HTTP_204_NO_CONTENT)

# ********************************** Manager2 Prim get post put delete **********************************
class Manager2PrimListCreateAPIView(generics.ListCreateAPIView):
    queryset = Manager2Prim.objects.all()
    serializer_class = Manager2PrimSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = Manager2PrimFilter
    permission_classes = [salary_permissions.Manager2PrimPermissions]

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            queryset = Manager2Prim.objects.all()
        elif request.user.company is not None:
            queryset = Manager2Prim.objects.filter(position__company=request.user.company)
        else:
            queryset = Manager2Prim.objects.all()
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
            prim_status = serializer.validated_data.get("prim_status")
            position = serializer.validated_data.get("position")
            prim = Manager2Prim.objects.filter(prim_status=prim_status, position=position)
            if len(prim)>0:
                return Response({"detail": "Bu status və vəzifəyə uyğun prim artıq əlavə olunub"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                serializer.save()
                return Response({"detail": "Prim əlavə edildi"})

class Manager2PrimDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Manager2Prim.objects.all()
    serializer_class = Manager2PrimSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = Manager2PrimFilter
    permission_classes = [salary_permissions.Manager2PrimPermissions]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "Manager2 bonus yeniləndi"}, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"detail": "Əməliyyat yerinə yetirildi"}, status=status.HTTP_204_NO_CONTENT)

# ********************************** Manager1 Prim New get post put delete **********************************
class Manager1PrimNewListCreateAPIView(generics.ListCreateAPIView):
    queryset = Manager1PrimNew.objects.all()
    serializer_class = Manager1PrimNewSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = Manager1PrimNewFilter
    permission_classes = [salary_permissions.Manager1PrimNewPermissions]

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            queryset = Manager1PrimNew.objects.all()
        elif request.user.company is not None:
            queryset = Manager1PrimNew.objects.filter(position__company=request.user.company)
        else:
            queryset = Manager1PrimNew.objects.all()
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
            prim_status = serializer.validated_data.get("prim_status")
            position = serializer.validated_data.get("position")
            prim = Manager1PrimNew.objects.filter(prim_status=prim_status, position=position)
            if len(prim)>0:
                return Response({"detail": "Bu status və vəzifəyə uyğun prim artıq əlavə olunub"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                serializer.save()
                return Response({"detail": "Prim əlavə edildi"})

class Manager1PrimNewDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Manager1PrimNew.objects.all()
    serializer_class = Manager1PrimNewSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = Manager1PrimNewFilter
    permission_classes = [salary_permissions.Manager1PrimNewPermissions]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "Manager1 bonus yeniləndi"}, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"detail": "Əməliyyat yerinə yetirildi"}, status=status.HTTP_204_NO_CONTENT)

# ********************************** Creditor Prim get post put delete **********************************
class CreditorPrimListCreateAPIView(generics.ListCreateAPIView):
    queryset = CreditorPrim.objects.all()
    serializer_class = CreditorPrimSerializer
    permission_classes = [salary_permissions.CreditorPrimPermissions]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({"detail": "Creditor prim əlavə olundu"}, status=status.HTTP_201_CREATED, headers=headers)

class CreditorPrimDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CreditorPrim.objects.all()
    serializer_class = CreditorPrimSerializer
    permission_classes = [salary_permissions.CreditorPrimPermissions]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "Kredit bonus faizi yeniləndi"}, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"detail": "Əməliyyat yerinə yetirildi"}, status=status.HTTP_204_NO_CONTENT)