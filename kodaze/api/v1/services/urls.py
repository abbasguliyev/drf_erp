from django.urls import path
from api.v1.services import views as services_views

urlpatterns = [
    path('service/', services_views.ServiceListCreateAPIView.as_view()),
    path('service/<int:pk>', services_views.ServiceDetailAPIView.as_view()),

    path('service-odeme/', services_views.ServicePaymentListCreateAPIView.as_view()),
    path('service-odeme/<int:pk>', services_views.ServicePaymentDetailAPIView.as_view()),

]