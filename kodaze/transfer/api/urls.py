from django.urls import path
from transfer.api import views as transfer_views

urlpatterns = [
    path('holding-transfer/', transfer_views.HoldingTransferListCreateAPIView.as_view()),
    path('company-transfer/', transfer_views.CompanyTransferListCreateAPIView.as_view()),
    path('office-transfer/', transfer_views.OfficeTransferListCreateAPIView.as_view()),
]