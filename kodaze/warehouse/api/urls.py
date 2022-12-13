from django.urls import path
from warehouse.api import views as warehouse_views

urlpatterns = [
    path('', warehouse_views.WarehouseListAPIView.as_view()),
    path('<int:pk>/', warehouse_views.WarehouseDetailAPIView.as_view()),

    path('warehouse-requests/', warehouse_views.WarehouseRequestListCreateAPIView.as_view()),
    path('warehouse-requests/<int:pk>/', warehouse_views.WarehouseRequestDetailAPIView.as_view()),

    path('stocks/', warehouse_views.StockListCreateAPIView.as_view()),

    path('holding-to-office-product-transfer/', warehouse_views.HoldingToOfficeProductTransfer.as_view()),
    path('office-to-holding-product-transfer/', warehouse_views.OfficeToHoldingProductTransfer.as_view()),
    path('between-office-product-transfer/', warehouse_views.BetweenOfficeProductTransfer.as_view()),

    path('change-unuseless-product/', warehouse_views.ChangeUnuselessOperationAPIView.as_view()),
    path('holding-warehouse/', warehouse_views.HoldingWarehouseAPIView.as_view()),
    path('holding-warehouse/<int:pk>/', warehouse_views.HoldingWarehouseRetriveAPIView.as_view()),
    path('holding-warehouse-delete/<int:pk>/', warehouse_views.HoldingWarehouseDestroyAPIView.as_view()),
    path('holding-warehouse-update/<int:pk>/', warehouse_views.HoldingWarehouseUpdateAPIView.as_view()),
    path('product-add-to-holding-warehouse/', warehouse_views.ProductAddToHoldigWarehouseAPIView.as_view()),
]