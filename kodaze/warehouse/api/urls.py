from django.urls import path
from warehouse.api import views as warehouse_views

urlpatterns = [
    path('', warehouse_views.WarehouseListAPIView.as_view()),
    path('<int:pk>/', warehouse_views.WarehouseDetailAPIView.as_view()),

    path('warehouse-requests/', warehouse_views.WarehouseRequestListCreateAPIView.as_view()),
    path('warehouse-requests/<int:pk>/', warehouse_views.WarehouseRequestDetailAPIView.as_view()),

    path('operations/', warehouse_views.OperationListCreateAPIView.as_view()),
    path('operations/<int:pk>/', warehouse_views.OperationDetailAPIView.as_view()),

    path('stocks/', warehouse_views.StockListCreateAPIView.as_view()),

    path('holding-office-transfer/', warehouse_views.HoldingOfficeProductTransfer.as_view()),

    path('change-unuseless-product/', warehouse_views.ChangeUnuselessOperationAPIView.as_view()),
    path('holding-warehouse/', warehouse_views.HoldingWarehouseAPIView.as_view()),
    path('product-add-to-holding-warehouse/', warehouse_views.ProductAddToHoldigWarehouseAPIView.as_view()),
]