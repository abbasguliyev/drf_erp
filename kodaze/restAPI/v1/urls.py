from django.conf import settings
from django.urls import include, path

from restAPI.v1.cashbox import views as cashbox_views
from restAPI.v1.holiday import views as holiday_views
from restAPI.v1.salary import views as salary_views
from restAPI.v1.services import views as services_views
from restAPI.v1.transfer import views as transfer_views
from restAPI.v1.warehouse import views as warehouse_views
from restAPI.v1.product import views as product_views
from restAPI.v1.income_expense import views as income_expense_views
from restAPI.v1.statistika import statistika

from rest_framework_simplejwt.views import token_refresh
from django.conf.urls.static import static

urlpatterns = [
    # account views *****************************************
    path('users/', include("restAPI.v1.account.urls")),

    # company views *****************************************
    path('company/', include("restAPI.v1.company.urls")),

    # contract views *****************************************
    path('contract/', include("restAPI.v1.contract.urls")),

    # backup views *****************************************
    path('backup/', include("restAPI.v1.backup_restore.urls")),

    # update views *****************************************
    path('update/', include("restAPI.v1.update.urls")),

    # task manager url *****************************************
    path('task-manager/', include("restAPI.v1.task_manager.urls")),

    # salary views *****************************************
    path('salary-goruntuleme/', salary_views.SalaryViewListCreateAPIView.as_view(),
         name="salary_goruntuleme"),
    path('salary-goruntuleme/<int:pk>', salary_views.SalaryViewDetailAPIView.as_view(),
         name="salary_goruntuleme_detail"),

    path('bonus/', salary_views.BonusListCreateAPIView.as_view(), name="bonus"),
    path('bonus/<int:pk>', salary_views.BonusDetailAPIView.as_view(),
         name="bonus_detail"),

    path('salary-ode/', salary_views.PaySalaryListCreateAPIView.as_view()),
    path('salary-ode/<int:pk>', salary_views.PaySalaryDetailAPIView.as_view()),

    path('advancepayment/', salary_views.AdvancePaymentListCreateAPIView.as_view(), name="advancepayment"),
    path('advancepayment/<int:pk>', salary_views.AdvancePaymentDetailAPIView.as_view(),
         name="advancepayment_detail"),

    path('salarydeduction/', salary_views.SalaryDeductionListCreateAPIView.as_view(), name="salarydeduction"),
    path('salarydeduction/<int:pk>', salary_views.SalaryDeductionDetailAPIView.as_view(),
         name="salarydeduction_detail"),

    path('office-leader-prim/',
         salary_views.OfficeLeaderPrimListCreateAPIView.as_view()),
    path('office-leader-prim/<int:pk>',
         salary_views.OfficeLeaderPrimDetailAPIView.as_view()),

    path('vanleader-prim/', salary_views.GroupLeaderPrimNewListCreateAPIView.as_view()),
    path('vanleader-prim/<int:pk>',
         salary_views.GroupLeaderPrimNewDetailAPIView.as_view()),

    path('canvasser-prim/', salary_views.Manager2PrimListCreateAPIView.as_view()),
    path('canvasser-prim/<int:pk>',
         salary_views.Manager2PrimDetailAPIView.as_view()),

    path('dealer-prim/', salary_views.Manager1PrimNewListCreateAPIView.as_view()),
    path('dealer-prim/<int:pk>', salary_views.Manager1PrimNewDetailAPIView.as_view()),

    path('creditor-prim/', salary_views.CreditorPrimListCreateAPIView.as_view()),
    path('creditor-prim/<int:pk>', salary_views.CreditorPrimDetailAPIView.as_view()),

    # working_day views *****************************************
    path('holding-working_day/', holiday_views.HoldingWorkingDayListCreateAPIView.as_view()),
    path('holding-working_day/<int:pk>',
         holiday_views.HoldingWorkingDayDetailAPIView.as_view()),
    path('holding-istisna-employee/',
         holiday_views.HoldingExceptionWorkerListCreateAPIView.as_view()),
    path('holding-istisna-employee/<int:pk>',
         holiday_views.HoldingExceptionWorkerDetailAPIView.as_view()),

    path('company-working_day/', holiday_views.CompanyWorkingDayListCreateAPIView.as_view()),
    path('company-working_day/<int:pk>',
         holiday_views.CompanyWorkingDayDetailAPIView.as_view()),
    path('company-istisna-employee/',
         holiday_views.CompanyExceptionWorkerListCreateAPIView.as_view()),
    path('company-istisna-employee/<int:pk>',
         holiday_views.CompanyExceptionWorkerDetailAPIView.as_view()),

    path('office-working_day/', holiday_views.OfficeWorkingDayListCreateAPIView.as_view()),
    path('office-working_day/<int:pk>', holiday_views.OfficeWorkingDayDetailAPIView.as_view()),
    path('office-istisna-employee/',
         holiday_views.OfficeExceptionWorkerListCreateAPIView.as_view()),
    path('office-istisna-employee/<int:pk>',
         holiday_views.OfficeExceptionWorkerDetailAPIView.as_view()),

    path('section-working_day/', holiday_views.SectionWorkingDayListCreateAPIView.as_view()),
    path('section-working_day/<int:pk>', holiday_views.SectionWorkingDayDetailAPIView.as_view()),
    path('section-istisna-employee/',
         holiday_views.SectionExceptionWorkerListCreateAPIView.as_view()),
    path('section-istisna-employee/<int:pk>',
         holiday_views.SectionExceptionWorkerDetailAPIView.as_view()),

    path('team-working_day/', holiday_views.TeamWorkingDayListCreateAPIView.as_view()),
    path('team-working_day/<int:pk>',
         holiday_views.TeamWorkingDayDetailAPIView.as_view()),
    path('team-istisna-employee/',
         holiday_views.TeamExceptionWorkerListCreateAPIView.as_view()),
    path('team-istisna-employee/<int:pk>',
         holiday_views.TeamExceptionWorkerDetailAPIView.as_view()),

    path('position-working_day/', holiday_views.PositionWorkingDayListCreateAPIView.as_view()),
    path('position-working_day/<int:pk>',
         holiday_views.PositionWorkingDayDetailAPIView.as_view()),
    path('position-istisna-employee/',
         holiday_views.PositionExceptionWorkerListCreateAPIView.as_view()),
    path('position-istisna-employee/<int:pk>',
         holiday_views.PositionExceptionWorkerDetailAPIView.as_view()),

    path('employee-working_day/', holiday_views.EmployeeWorkingDayListCreateAPIView.as_view()),
    path('employee-working_day/<int:pk>', holiday_views.EmployeeWorkingDayDetailAPIView.as_view()),

    path('employee-gelib-getme-vaxtlari/',
         holiday_views.EmployeeArrivalAndDepartureTimesListCreateAPIView.as_view()),
    path('employee-gelib-getme-vaxtlari/<int:pk>',
         holiday_views.EmployeeArrivalAndDepartureTimesDetailAPIView.as_view()),

    # cashbox views *****************************************
    path('pul-axini/', cashbox_views.CashFlowListAPIView.as_view(), name="pul_axini"),
    path('pul-axini/<int:pk>', cashbox_views.CashFlowDetailAPIView.as_view(),
         name="pul_axini_detail"),

    path('holding-kassa/', cashbox_views.HoldingCashboxListCreateAPIView.as_view(),
         name="cashbox"),
    path('holding-kassa/<int:pk>', cashbox_views.HoldingCashboxDetailAPIView.as_view(),
         name="cashbox_detail"),

    path('company-kassa/', cashbox_views.CompanyCashboxListCreateAPIView.as_view(),
         name="cashbox"),
    path('company-kassa/<int:pk>', cashbox_views.CompanyCashboxDetailAPIView.as_view(),
         name="cashbox_detail"),

    path('office-kassa/', cashbox_views.OfficeCashboxListCreateAPIView.as_view(),
         name="cashbox"),
    path('office-kassa/<int:pk>', cashbox_views.OfficeCashboxDetailAPIView.as_view(),
         name="cashbox_detail"),

    # transfer_views ***************************************
    path('company-holding-transfer/', transfer_views.TransferFromCompanyToHoldingListCreateAPIView.as_view(),
         name="company_holding_transfer"),
    path('company-holding-transfer/<int:pk>', transfer_views.TransferFromCompanyToHoldingDetailAPIView.as_view(),
         name="company_holding_transfer_detail"),

    path('holding-company-transfer/', transfer_views.TransferFromHoldingToCompanyListCreateAPIView.as_view(),
         name="holding_company_transfer"),
    path('holding-company-transfer/<int:pk>', transfer_views.TransferFromHoldingToCompanyDetailAPIView.as_view(),
         name="holding_company_transfer_detail"),

    path('company-office-transfer/', transfer_views.TransferFromCompanyToOfficesListCreateAPIView.as_view(),
         name="offices_transfer"),
    path('company-office-transfer/<int:pk>', transfer_views.TransferFromCompanyToOfficesDetailAPIView.as_view(),
         name="offices_transfer_detail"),

    path('office-company-transfer/', transfer_views.TransferFromOfficeToCompanyListCreateAPIView.as_view(),
         name="office_company_transfer"),
    path('office-company-transfer/<int:pk>', transfer_views.TransferFromOfficeToCompanyDetailAPIView.as_view(),
         name="office_company_transfer_detail"),

    # income_expense_views *********************************
    path('holding-kassa-income/', income_expense_views.HoldingCashboxIncomeListCreateAPIView.as_view(),
         name="cashbox_income"),
    path('holding-kassa-income/<int:pk>', income_expense_views.HoldingCashboxIncomeDetailAPIView.as_view(),
         name="cashbox_income_detail"),

    path('holding-kassa-expense/', income_expense_views.HoldingCashboxExpenseListCreateAPIView.as_view(),
         name="cashbox_expense"),
    path('holding-kassa-expense/<int:pk>', income_expense_views.HoldingCashboxExpenseDetailAPIView.as_view(),
         name="cashbox_expense_detail"),

    path('company-kassa-income/', income_expense_views.CompanyCashboxIncomeListCreateAPIView.as_view(),
         name="cashbox_income"),
    path('company-kassa-income/<int:pk>', income_expense_views.CompanyCashboxIncomeDetailAPIView.as_view(),
         name="cashbox_income_detail"),

    path('company-kassa-expense/', income_expense_views.CompanyCashboxExpenseListCreateAPIView.as_view(),
         name="cashbox_expense"),
    path('company-kassa-expense/<int:pk>', income_expense_views.CompanyCashboxExpenseDetailAPIView.as_view(),
         name="cashbox_expense_detail"),

    path('office-kassa-income/', income_expense_views.OfficeCashboxIncomeListCreateAPIView.as_view(),
         name="cashbox_income"),
    path('office-kassa-income/<int:pk>', income_expense_views.OfficeCashboxIncomeDetailAPIView.as_view(),
         name="cashbox_income_detail"),

    path('office-kassa-expense/', income_expense_views.OfficeCashboxExpenseListCreateAPIView.as_view(),
         name="cashbox_expense"),
    path('office-kassa-expense/<int:pk>', income_expense_views.OfficeCashboxExpenseDetailAPIView.as_view(),
         name="cashbox_expense_detail"),

    # product_views *****************************************
    path('product/', product_views.ProductListCreateAPIView.as_view(),
         name="product"),
    path('product/<int:pk>', product_views.ProductDetailAPIView.as_view(),
         name="product_detail"),

    # warehouse_views *****************************************
    path('warehouse/', warehouse_views.WarehouseListCreateAPIView.as_view(), name="warehouse"),
    path('warehouse/<int:pk>', warehouse_views.WarehouseDetailAPIView.as_view(),
         name="warehouse_detail"),

    path('warehouse-noteler/', warehouse_views.WarehouseRequestListCreateAPIView.as_view(),
         name="warehouse_noteler"),
    path('warehouse-noteler/<int:pk>', warehouse_views.WarehouseRequestDetailAPIView.as_view(),
         name="warehouse_noteler_detail"),

    path('operation/', warehouse_views.OperationListCreateAPIView.as_view(),
         name="operation"),
    path('operation/<int:pk>', warehouse_views.OperationDetailAPIView.as_view(),
         name="operation_detail"),

    path('stok/', warehouse_views.StockListCreateAPIView.as_view(), name="stok"),
    path('stok/<int:pk>', warehouse_views.StockDetailAPIView.as_view(),
         name="stok_detail"),

    # services_views *****************************************
    path('service/', services_views.ServiceListCreateAPIView.as_view(), name="service"),
    path('service/<int:pk>', services_views.ServiceDetailAPIView.as_view(),
         name="service_detail"),

    path('service-odeme/', services_views.ServicePaymentListCreateAPIView.as_view()),
    path('service-odeme/<int:pk>', services_views.ServicePaymentDetailAPIView.as_view()),

    # statistika views *****************************************
    path('statistika/sale-quantityi', statistika.SalaryViewStatistikaAPIView.as_view(),
         name="sale_quantity_statistika"),
    path('statistika/demo-statistika',
         statistika.DemoStatistikaListAPIView.as_view(), name="demo_statistika"),
    path('statistika/contract-statistika',
         statistika.ContractStatistikaAPIView.as_view(), name="contract_statistika"),
    path('statistika/user-statistika',
         statistika.UserStatistikaList.as_view(), name="user_statistika"),
    path('statistika/service-statistika',
         statistika.ServiceStatistikaAPIView.as_view(), name="service_statistika"),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
