from django.urls import path
from contract.api import views as contract_views

urlpatterns = [
    path('test-installment/', contract_views.CreateTestInstallmentAPIView.as_view()),
    
    path('', contract_views.ContractListAPIView.as_view()),
    path('create/', contract_views.ContractCreateAPIView.as_view()),
    path('<int:pk>/', contract_views.ContractDetailAPIView.as_view()),
    path('update/<int:pk>/', contract_views.ContractUpdateAPIView.as_view()),
    path('pay-initial-debt/', contract_views.PayInitialPaymentDebtAPIView.as_view()),
    path('remove-contract/', contract_views.RemoveProductAPIView.as_view()),

    path('creditors/', contract_views.ContractCreditorListCreateAPIView.as_view()),
    path('creditors/<int:pk>/', contract_views.ContractCreditorDetailAPIView.as_view()),

    path('change-product-of-contract/', contract_views.ContractChangeListCreateAPIView.as_view()),
    path('find-contract-paid-amount/', contract_views.FindContractPaidAmout.as_view()),

    path('installments/', contract_views.InstallmentListAPIView.as_view()),
    path('pay-installments/', contract_views.PayInstallmentAPIView.as_view()),
    path('installments/<int:pk>/', contract_views.InstallmentDetailAPIView.as_view()),

    path('gifts/', contract_views.ContractGiftListAPIView.as_view()),
    path('gift-add/', contract_views.ContractGiftCreateAPIView.as_view()),
    path('gifts/<int:pk>/', contract_views.ContractGiftDetailAPIView.as_view()),

    path('demo/', contract_views.DemoSalesListAPIView.as_view()),
    path('demo/<int:pk>/', contract_views.DemoSalesDetailAPIView.as_view()),
]
