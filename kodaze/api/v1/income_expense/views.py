from rest_framework import status, generics
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.response import Response

from api.v1.income_expense.serializers import (
    OfficeCashboxIncomeSerializer,
    OfficeCashboxExpenseSerializer,
    CompanyCashboxIncomeSerializer,
    CompanyCashboxExpenseSerializer,
    HoldingCashboxIncomeSerializer,
    HoldingCashboxExpenseSerializer
)


from income_expense.models import (
    HoldingCashboxIncome,
    HoldingCashboxExpense,
    OfficeCashboxIncome,
    OfficeCashboxExpense,
    CompanyCashboxIncome,
    CompanyCashboxExpense,
)

from api.v1.income_expense import utils as income_expense_utils
from api.v1.income_expense.filters import (
    HoldingCashboxIncomeFilter,
    HoldingCashboxExpenseFilter,
    OfficeCashboxIncomeFilter,
    OfficeCashboxExpenseFilter,
    CompanyCashboxIncomeFilter,
    CompanyCashboxExpenseFilter,
)

from api.v1.income_expense import permissions as company_permissions

# ********************************** holding kassa income, expense put delete post get **********************************

class HoldingCashboxIncomeListCreateAPIView(generics.ListCreateAPIView):
    queryset = HoldingCashboxIncome.objects.all()
    serializer_class = HoldingCashboxIncomeSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = HoldingCashboxIncomeFilter
    permission_classes = [company_permissions.HoldingCashboxIncomePermissions]

    def create(self, request, *args, **kwargs):
        return income_expense_utils.holding_cashbox_income_create(self, request, *args, **kwargs)


class HoldingCashboxIncomeDetailAPIView(generics.RetrieveAPIView):
    queryset = HoldingCashboxIncome.objects.all()
    serializer_class = HoldingCashboxIncomeSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = HoldingCashboxIncomeFilter
    permission_classes = [company_permissions.HoldingCashboxIncomePermissions]



# **********************************

class HoldingCashboxExpenseListCreateAPIView(generics.ListCreateAPIView):
    queryset = HoldingCashboxExpense.objects.all()
    serializer_class = HoldingCashboxExpenseSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = HoldingCashboxExpenseFilter
    permission_classes = [company_permissions.HoldingCashboxExpensePermissions]

    def create(self, request, *args, **kwargs):
        return income_expense_utils.holding_cashbox_expense_create(self, request, *args, **kwargs)


class HoldingCashboxExpenseDetailAPIView(generics.RetrieveAPIView):
    queryset = HoldingCashboxExpense.objects.all()
    serializer_class = HoldingCashboxExpenseSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = HoldingCashboxExpenseFilter
    permission_classes = [company_permissions.HoldingCashboxExpensePermissions]



# ********************************** company kassa income, expense put delete post get **********************************

class CompanyCashboxIncomeListCreateAPIView(generics.ListCreateAPIView):
    queryset = CompanyCashboxIncome.objects.all()
    serializer_class = CompanyCashboxIncomeSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CompanyCashboxIncomeFilter
    permission_classes = [company_permissions.CompanyCashboxIncomePermissions]

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            queryset = CompanyCashboxIncome.objects.all()
        elif request.user.company is not None:
            queryset = CompanyCashboxIncome.objects.filter(cashbox__company=request.user.company)
        else:
            queryset = CompanyCashboxIncome.objects.all()
        queryset = self.filter_queryset(queryset)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


    def create(self, request, *args, **kwargs):
        return income_expense_utils.cashbox_income_create(self, request, *args, **kwargs)


class CompanyCashboxIncomeDetailAPIView(generics.RetrieveAPIView):
    queryset = CompanyCashboxIncome.objects.all()
    serializer_class = CompanyCashboxIncomeSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CompanyCashboxIncomeFilter
    permission_classes = [company_permissions.CompanyCashboxIncomePermissions]



# **********************************

class CompanyCashboxExpenseListCreateAPIView(generics.ListCreateAPIView):
    queryset = CompanyCashboxExpense.objects.all()
    serializer_class = CompanyCashboxExpenseSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CompanyCashboxExpenseFilter
    permission_classes = [company_permissions.CompanyCashboxExpensePermissions]

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            queryset = CompanyCashboxExpense.objects.all()
        elif request.user.company is not None:
            queryset = CompanyCashboxExpense.objects.filter(cashbox__company=request.user.company)
        else:
            queryset = CompanyCashboxExpense.objects.all()
        queryset = self.filter_queryset(queryset)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        return income_expense_utils.cashbox_expense_create(self, request, *args, **kwargs)


class CompanyCashboxExpenseDetailAPIView(generics.RetrieveAPIView):
    queryset = CompanyCashboxExpense.objects.all()
    serializer_class = CompanyCashboxExpenseSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CompanyCashboxExpenseFilter
    permission_classes = [company_permissions.CompanyCashboxExpensePermissions]



# ********************************** Office kassa income, expense put delete post get **********************************

class OfficeCashboxIncomeListCreateAPIView(generics.ListCreateAPIView):
    queryset = OfficeCashboxIncome.objects.all()
    serializer_class = OfficeCashboxIncomeSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = OfficeCashboxIncomeFilter
    permission_classes = [company_permissions.OfficeCashboxIncomePermissions]

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            queryset = OfficeCashboxIncome.objects.all()
        elif request.user.company is not None:
            if request.user.office is not None:
                queryset = OfficeCashboxIncome.objects.filter(cashbox__office__company=request.user.company, cashbox__office=request.user.office)
            queryset = OfficeCashboxIncome.objects.filter(cashbox__office__company=request.user.company)
        else:
            queryset = OfficeCashboxIncome.objects.all()
        queryset = self.filter_queryset(queryset)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        return income_expense_utils.office_cashbox_income_create(self, request, *args, **kwargs)


class OfficeCashboxIncomeDetailAPIView(generics.RetrieveAPIView):
    queryset = OfficeCashboxIncome.objects.all()
    serializer_class = OfficeCashboxIncomeSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = OfficeCashboxIncomeFilter
    permission_classes = [company_permissions.OfficeCashboxIncomePermissions]



# **********************************

class OfficeCashboxExpenseListCreateAPIView(generics.ListCreateAPIView):
    queryset = OfficeCashboxExpense.objects.all()
    serializer_class = OfficeCashboxExpenseSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = OfficeCashboxExpenseFilter
    permission_classes = [company_permissions.OfficeCashboxExpensePermissions]

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            queryset = OfficeCashboxExpense.objects.all()
        elif request.user.company is not None:
            if request.user.office is not None:
                queryset = OfficeCashboxExpense.objects.filter(cashbox__office__company=request.user.company, cashbox__office=request.user.office)
            queryset = OfficeCashboxExpense.objects.filter(cashbox__office__company=request.user.company)
        else:
            queryset = OfficeCashboxExpense.objects.all()
        queryset = self.filter_queryset(queryset)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        return income_expense_utils.office_cashbox_expense_create(self, request, *args, **kwargs)


class OfficeCashboxExpenseDetailAPIView(generics.RetrieveAPIView):
    queryset = OfficeCashboxExpense.objects.all()
    serializer_class = OfficeCashboxExpenseSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = OfficeCashboxExpenseFilter
    permission_classes = [company_permissions.OfficeCashboxExpensePermissions]
