from api.v1.salary.services.advancedpayment_service import advancepayment_create
from api.v1.salary.services.bonus_service import bonus_create
from api.v1.salary.services.commission_services import (
    month_range_create,
    sale_range_create,
    commission_installment_create,
    commission_sale_range_create,
    commission_create,
    commission_update
)
from api.v1.salary.services.salary_pay_service import salary_pay_create
from api.v1.salary.services.salarydeduction_service import salarydeduction_create
from api.v1.salary.services.salarypunishment_service import salarypunishment_create
from api.v1.salary.utils import salary_operation_delete

from salary.models import (
    AdvancePayment,
    SalaryDeduction,
    Bonus,
    SalaryPunishment,
    SalaryView,
    PaySalary,
    MonthRange, SaleRange, Commission, CommissionInstallment, CommissionSaleRange
)

from holiday.models import EmployeeWorkingDay

from api.v1.salary.serializers import (
    AdvancePaymentSerializer,
    BonusSerializer,
    SalaryDeductionSerializer,
    SalaryPunishmentSerializer,
    SalaryViewSerializer,
    PaySalarySerializer,
    MonthRangeSerializer, SaleRangeSerializer, CommissionSerializer,
    CommissionInstallmentSerializer, CommissionSaleRangeSerializer,
)

from api.v1.account.serializers import UserSerializer

from rest_framework import status, generics

from rest_framework.response import Response

from api.v1.salary import permissions as salary_permissions

from django_filters.rest_framework import DjangoFilterBackend

from api.v1.salary.filters import (
    AdvancePaymentFilter,
    BonusFilter,
    SalaryDeductionFilter,
    SalaryPunishmentFilter,
    SalaryViewFilter,
    PaySalaryFilter,
)

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie

from django.contrib.auth import get_user_model

User = get_user_model()

# ********************************** AdvancePayment get post put delete **********************************


class AdvancePaymentListCreateAPIView(generics.ListCreateAPIView):
    queryset = AdvancePayment.objects.select_related('employee').all()
    serializer_class = AdvancePaymentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = AdvancePaymentFilter
    permission_classes = [salary_permissions.AdvancePaymentPermissions]

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            queryset = self.queryset
        elif request.user.company is not None:
            if request.user.office is not None:
                queryset = self.queryset.filter(employee__company=request.user.company,
                                                employee__office=request.user.office)
            queryset = self.queryset.filter(
                employee__company=request.user.company)
        else:
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
        if (serializer.is_valid()):
            user = request.user
            advancepayment_create(user, **serializer.validated_data)
            return Response({"detail": "Avans vermə əməliyyatı yerinə yetirildi"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"detail": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class AdvancePaymentDetailAPIView(generics.RetrieveDestroyAPIView):
    queryset = AdvancePayment.objects.all()
    serializer_class = AdvancePaymentSerializer
    permission_classes = [salary_permissions.AdvancePaymentPermissions]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        salary_operation_delete(instance=instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


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
                queryset = SalaryDeduction.objects.filter(employee__company=request.user.company,
                                                          employee__office=request.user.office)
            queryset = SalaryDeduction.objects.filter(
                employee__company=request.user.company)
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
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            salarydeduction_create(**serializer.validated_data)
            return Response({"detail": "Kəsinti əməliyyatı yerinə yetirildi"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"detail": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class SalaryDeductionDetailAPIView(generics.RetrieveDestroyAPIView):
    queryset = SalaryDeduction.objects.all()
    serializer_class = SalaryDeductionSerializer
    permission_classes = [salary_permissions.SalaryDeductionPermissions]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        salary_operation_delete(instance=instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

# ********************************** SalaryPunishment get post put delete **********************************
class SalaryPunishmentListCreateAPIView(generics.ListCreateAPIView):
    queryset = SalaryPunishment.objects.all()
    serializer_class = SalaryPunishmentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = SalaryPunishmentFilter
    permission_classes = [salary_permissions.SalaryPunishmentPermissions]

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            queryset = self.queryset
        elif request.user.company is not None:
            if request.user.office is not None:
                queryset = self.queryset.filter(employee__company=request.user.company,
                                                employee__office=request.user.office)
            queryset = self.queryset.filter(
                employee__company=request.user.company)
        else:
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
        if (serializer.is_valid()):
            salarypunishment_create(**serializer.validated_data)
            return Response({"detail": "Cərimə əməliyyatı yerinə yetirildi"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"detail": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class SalaryPunishmentDetailAPIView(generics.RetrieveDestroyAPIView):
    queryset = SalaryPunishment.objects.all()
    serializer_class = SalaryPunishmentSerializer
    permission_classes = [salary_permissions.SalaryPunishmentPermissions]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        salary_operation_delete(instance=instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

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
                queryset = Bonus.objects.filter(employee__company=request.user.company,
                                                employee__office=request.user.office)
            queryset = Bonus.objects.filter(
                employee__company=request.user.company)
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
        serializer = self.get_serializer(data=request.data)
        if (serializer.is_valid()):
            bonus_create(**serializer.validated_data)
            return Response({"detail": "Bonus əlavə olundu"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"detail": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class BonusDetailAPIView(generics.RetrieveDestroyAPIView):
    queryset = Bonus.objects.all()
    serializer_class = BonusSerializer
    permission_classes = [salary_permissions.BonusPermissions]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        salary_operation_delete(instance=instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

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
                queryset = PaySalary.objects.filter(employee__company=request.user.company,
                                                    employee__office=request.user.office)
            queryset = PaySalary.objects.filter(
                employee__company=request.user.company)
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
        serializer = self.get_serializer(data=request.data)
        if (serializer.is_valid()):
            user = request.user
            salary_pay_create(user, **serializer.validated_data)
            return Response({"detail": "Maaş ödəmə yerinə yetirildi"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"detail": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class PaySalaryDetailAPIView(generics.RetrieveAPIView):
    queryset = PaySalary.objects.all()
    serializer_class = PaySalarySerializer
    permission_classes = [salary_permissions.PaySalaryPermissions]


# ********************************** SalaryView get post put delete **********************************
class SalaryViewListCreateAPIView(generics.ListAPIView):
    queryset = SalaryView.objects.select_related('employee').all()
    serializer_class = SalaryViewSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = SalaryViewFilter
    permission_classes = [salary_permissions.SalaryViewPermissions]

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            queryset = self.queryset
        elif request.user.company is not None:
            if request.user.office is not None:
                queryset = self.queryset.filter(employee__company=request.user.company,
                                                employee__office=request.user.office)
            queryset = self.queryset.filter(
                employee__company=request.user.company)
        else:
            queryset = self.queryset

        queryset = self.filter_queryset(queryset)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)

            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)


class SalaryViewDetailAPIView(generics.RetrieveDestroyAPIView):
    queryset = SalaryView.objects.all()
    serializer_class = SalaryViewSerializer
    permission_classes = [salary_permissions.SalaryViewPermissions]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"detail": "Əməliyyat yerinə yetirildi"}, status=status.HTTP_204_NO_CONTENT)


# ********************************** Commission get post put delete **********************************
class MonthRangeListCreateAPIView(generics.ListCreateAPIView):
    queryset = MonthRange.objects.all()
    serializer_class = MonthRangeSerializer
    permission_classes = [salary_permissions.MonthRangePermissions]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if (serializer.is_valid()):
            month_range_create(**serializer.validated_data)
            return Response({"detail": "Ay aralığı əlavə edildi"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"detail": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class MonthRangeDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MonthRange.objects.all()
    serializer_class = MonthRangeSerializer
    permission_classes = [salary_permissions.MonthRangePermissions]


class SaleRangeListCreateAPIView(generics.ListCreateAPIView):
    queryset = SaleRange.objects.all()
    serializer_class = SaleRangeSerializer
    permission_classes = [salary_permissions.SaleRangePermissions]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if (serializer.is_valid()):
            sale_range_create(**serializer.validated_data)
            return Response({"detail": "Satış sayı aralığı əlavə edildi"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"detail": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class SaleRangeDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SaleRange.objects.all()
    serializer_class = SaleRangeSerializer
    permission_classes = [salary_permissions.SaleRangePermissions]


class CommissionInstallmentListCreateAPIView(generics.ListCreateAPIView):
    queryset = CommissionInstallment.objects.all()
    serializer_class = CommissionInstallmentSerializer
    # permission_classes = [salary_permissions.CommissionInstallmentPermissions]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if (serializer.is_valid()):
            commission_installment_create(**serializer.validated_data)
            return Response({"detail": "Əməliyyat yerinə yetirildi"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"detail": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class CommissionInstallmentDetailAPIView(generics.ListCreateAPIView):
    queryset = CommissionInstallment.objects.all()
    serializer_class = CommissionInstallmentSerializer
    # permission_classes = [salary_permissions.CommissionInstallmentPermissions]


class CommissionSaleRangeListCreateAPIView(generics.ListCreateAPIView):
    queryset = CommissionSaleRange.objects.all()
    serializer_class = CommissionSaleRangeSerializer
    # permission_classes = [salary_permissions.CommissionSaleRangePermissions]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if (serializer.is_valid()):
            commission_sale_range_create(**serializer.validated_data)
            return Response({"detail": "Əməliyyat yerinə yetirildi"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"detail": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class CommissionSaleRangeDetailAPIView(generics.ListCreateAPIView):
    queryset = CommissionSaleRange.objects.all()
    serializer_class = CommissionSaleRangeSerializer
    # permission_classes = [salary_permissions.CommissionSaleRangePermissions]


class CommissionListCreateAPIView(generics.ListCreateAPIView):
    queryset = Commission.objects.all()
    serializer_class = CommissionSerializer
    permission_classes = [salary_permissions.CommissionPermissions]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if (serializer.is_valid()):
            commission_create(**serializer.validated_data)
            return Response({"detail": "Komissiya əlavə edildi"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"detail": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class CommissionDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Commission.objects.all()
    serializer_class = CommissionSerializer
    permission_classes = [salary_permissions.CommissionPermissions]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            commission_update(instance.id, **serializer.validated_data)
            return Response({"detail": "Əməliyyat yerinə yetirildi"}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

# import xlwt

# from django.http import HttpResponse
# from django.http import FileResponse
# from rest_framework.views import APIView


# class ExportData(APIView):
    
#     def post(self, request, format=None):
#         response = HttpResponse(content_type='application/ms-excel')
#         response['Content-Disposition'] = 'attachment; filename="users.xls"'

#         wb = xlwt.Workbook(encoding='utf-8')
#         ws = wb.add_sheet('Users')

#         # Sheet header, first row
#         row_num = 0

#         font_style = xlwt.XFStyle()
#         font_style.font.bold = True

#         columns = ['Fullname', 'Company', 'Office', 'Position']

#         for col_num in range(len(columns)):
#             ws.write(row_num, col_num, columns[col_num], font_style)

#         # Sheet body, remaining rows
#         font_style = xlwt.XFStyle()
#         print(f"{request=}")
#         print(f"{request.data=}")
#         rows = request.data
#         for row in rows:
#             row_num += 1
#             row_list = list()
#             try:
#                 fullname = row.get('employee').get('fullname')
#             except:
#                 fullname = None
#             try:
#                 company = row.get('company').get('name')
#             except:
#                 company = None
#             try:
#                 office = row.get('office').get('name')
#             except:
#                 office = None
#             try:
#                 position = row.get('position').get('name')
#             except:
#                 position = None
#             row_list.append(fullname)
#             row_list.append(company)
#             row_list.append(office)
#             row_list.append(position)
#             for col_num in range(len(row_list)):
#                 ws.write(row_num, col_num, row_list[col_num], font_style)

#         wb.save(response)
#         path = "/home/abbas/Workspace/kodazeERP"
#         return FileResponse(filename=f"{path}/{wb}", as_attachment=True)
