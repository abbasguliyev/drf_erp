from django.urls import path
from cashbox.api import views as cashbox_views


urlpatterns = [
    path('cashflow/', cashbox_views.CashFlowListAPIView.as_view()),
    path('cashflow/<int:pk>/', cashbox_views.CashFlowDetailAPIView.as_view()),

    path('holding-cashbox/', cashbox_views.HoldingCashboxListCreateAPIView.as_view()),
    path('holding-cashbox/<int:pk>/', cashbox_views.HoldingCashboxDetailAPIView.as_view()),

    path('company-cashbox/', cashbox_views.CompanyCashboxListCreateAPIView.as_view()),
    path('company-cashbox/<int:pk>/', cashbox_views.CompanyCashboxDetailAPIView.as_view()),

    path('office-cashbox/', cashbox_views.OfficeCashboxListCreateAPIView.as_view()),
    path('office-cashbox/<int:pk>/', cashbox_views.OfficeCashboxDetailAPIView.as_view()),

    path('holding-cashbox-operation/', cashbox_views.HoldingCashboxOperationListCreateAPIView.as_view()),
    path('company-cashbox-operation/', cashbox_views.CompanyCashboxOperationListCreateAPIView.as_view()),

    path('cost-type/', cashbox_views.CostTypeListApiView.as_view()),
    path('cost-type/create/', cashbox_views.CostTypeCreateApiView.as_view()),
    path('cost-type/<int:pk>/', cashbox_views.CostTypeDetailApiView.as_view()),

    path('installment-payment-tracking/', cashbox_views.InstallmentPaymentTrackingListAPIView.as_view()),
    path('service-payment-tracking/', cashbox_views.ServicePaymentTrackingListAPIView.as_view()),
]