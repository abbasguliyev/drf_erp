from django.urls import path
from api.v1.warehouse import views as warehouse_views

urlpatterns = [
    path('', warehouse_views.WarehouseListCreateAPIView.as_view()),
    path('<int:pk>/', warehouse_views.WarehouseDetailAPIView.as_view()),

    path('warehouse-requests/', warehouse_views.WarehouseRequestListCreateAPIView.as_view()),
    path('warehouse-requests/<int:pk>/', warehouse_views.WarehouseRequestDetailAPIView.as_view()),

    path('operations/', warehouse_views.OperationListCreateAPIView.as_view()),
    path('operations/<int:pk>/', warehouse_views.OperationDetailAPIView.as_view()),

    path('stocks/', warehouse_views.StockListCreateAPIView.as_view()),
    path('stocks/<int:pk>/', warehouse_views.StockDetailAPIView.as_view()),
]