from django.urls import path
from restAPI.v1.contract import views as contract_views

urlpatterns = [
    path('test-installment/', contract_views.create_test_installment),
    
    path('', contract_views.ContractListCreateAPIView.as_view()),
    path('<int:pk>/', contract_views.ContractDetailAPIView.as_view()),

    path('creditors/', contract_views.ContractCreditorListCreateAPIView.as_view()),
    path('creditors/<int:pk>/', contract_views.ContractCreditorDetailAPIView.as_view()),

    path('change-product-of-contract/', contract_views.ContractChangeListCreateAPIView.as_view()),

    path('installments/', contract_views.InstallmentListCreateAPIView.as_view()),
    path('installments/<int:pk>/', contract_views.InstallmentDetailAPIView.as_view()),

    path('gifts/', contract_views.ContractGiftListCreateAPIView.as_view()),
    path('gifts/<int:pk>/', contract_views.ContractGiftDetailAPIView.as_view()),

    path('demo/', contract_views.DemoSalesListAPIView.as_view()),
    path('demo/<int:pk>/', contract_views.DemoSalesDetailAPIView.as_view()),
]
