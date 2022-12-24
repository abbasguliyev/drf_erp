from django.urls import path
from services.api import views as services_views

urlpatterns = [
    path('', services_views.ServiceListCreateAPIView.as_view()),
    path('<int:pk>/', services_views.ServiceDetailAPIView.as_view()),

    path('service-payment/', services_views.ServicePaymentListCreateAPIView.as_view()),
    path('service-payment/<int:pk>', services_views.ServicePaymentDetailAPIView.as_view()),

    path('periodic-product-operation/', services_views.ServiceProductForContractOperation.as_view()),
    path('periodic-products/', services_views.ServiceProductForContractListAPIView.as_view()),
    path('periodic-products/<int:pk>', services_views.ServiceProductForContractRetriveDestroyAPIView.as_view()),
]