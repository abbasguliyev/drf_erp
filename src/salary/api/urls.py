from django.urls import path
from salary.api import views as salary_views

urlpatterns = [
    path('salary-views/', salary_views.SalaryViewListAPIView.as_view()),
    path('salary-views/<int:pk>/', salary_views.SalaryViewDetailAPIView.as_view()),

    path('bonus/', salary_views.BonusListCreateAPIView.as_view()),
    path('bonus/<int:pk>/', salary_views.BonusDetailAPIView.as_view()),
    path('bonus-delete/', salary_views.BonusDelete.as_view()),

    path('pay-salary/', salary_views.PaySalaryCreateAPIView.as_view()),

    path('advancepayment/', salary_views.AdvancePaymentListCreateAPIView.as_view()),
    path('advancepayment/<int:pk>/', salary_views.AdvancePaymentDetailAPIView.as_view()),

    path('salary-deduction/', salary_views.SalaryDeductionListCreateAPIView.as_view()),
    path('salary-deduction/<int:pk>/', salary_views.SalaryDeductionDetailAPIView.as_view()),
    path('salary-deduction-delete/', salary_views.SalaryDeductionDelete.as_view()),
    
    path('salary-punishment/', salary_views.SalaryPunishmentListCreateAPIView.as_view()),
    path('salary-punishment/<int:pk>/', salary_views.SalaryPunishmentDetailAPIView.as_view()),
    path('salary-punishment-delete/', salary_views.SalaryPunishmentDelete.as_view()),

    path('month-range/',salary_views.MonthRangeListCreateAPIView.as_view()),
    path('month-range/<int:pk>/', salary_views.MonthRangeDetailAPIView.as_view()),

    path('sale-range/',salary_views.SaleRangeListCreateAPIView.as_view()),
    path('sale-range/<int:pk>/', salary_views.SaleRangeDetailAPIView.as_view()),

    path('commission-installment/',salary_views.CommissionInstallmentListCreateAPIView.as_view()),
    path('commission-installment/<int:pk>/', salary_views.CommissionInstallmentDetailAPIView.as_view()),

    path('commission-sale-range/',salary_views.CommissionSaleRangeListCreateAPIView.as_view()),
    path('commission-sale-range/<int:pk>/', salary_views.CommissionSaleRangeDetailAPIView.as_view()),

    path('commission/',salary_views.CommissionListCreateAPIView.as_view()),
    path('commission/<int:pk>/', salary_views.CommissionDetailAPIView.as_view()),

    path('employee-activity/', salary_views.EmployeeActivityListAPIView.as_view()),

    path('export-data/', salary_views.ExportData.as_view(), name='export_users_xls'),

]