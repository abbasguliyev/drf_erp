from django.urls import path
from restAPI.v1.cashbox import views as cashbox_views


urlpatterns = [
    path('cashflow/', cashbox_views.CashFlowListAPIView.as_view()),
    path('cashflow/<int:pk>', cashbox_views.CashFlowDetailAPIView.as_view()),

    path('holding-cashbox/', cashbox_views.HoldingCashboxListCreateAPIView.as_view()),
    path('holding-cashbox/<int:pk>', cashbox_views.HoldingCashboxDetailAPIView.as_view()),

    path('company-cashbox/', cashbox_views.CompanyCashboxListCreateAPIView.as_view()),
    path('company-cashbox/<int:pk>', cashbox_views.CompanyCashboxDetailAPIView.as_view()),

    path('office-cashbox/', cashbox_views.OfficeCashboxListCreateAPIView.as_view()),
    path('office-cashbox/<int:pk>', cashbox_views.OfficeCashboxDetailAPIView.as_view()),
]