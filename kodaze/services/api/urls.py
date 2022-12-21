from django.urls import path
from services.api import views as services_views

urlpatterns = [
    path('', services_views.ServiceListCreateAPIView.as_view()),
    path('<int:pk>', services_views.ServiceDetailAPIView.as_view()),

    path('service-payment/', services_views.ServicePaymentListCreateAPIView.as_view()),
    path('service-payment/<int:pk>', services_views.ServicePaymentDetailAPIView.as_view()),
]