from django.urls import path
from restAPI.v1.contract import views as contract_views

urlpatterns = [
    path('test-installment/', contract_views.create_test_kredit),
    path('', contract_views.MuqavileListCreateAPIView.as_view()),
    path('<int:pk>/', contract_views.MuqavileDetailAPIView.as_view()),

    path('creditors/', contract_views.MuqavileKreditorListCreateAPIView.as_view()),
    path('creditors/<int:pk>/', contract_views.MuqavileKreditorDetailAPIView.as_view()),

    path('change-product-of-contract/', contract_views.DeyisimListCreateAPIView.as_view()),

    path('installments/', contract_views.OdemeTarixListCreateAPIView.as_view()),
    path('installments/<int:pk>/', contract_views.OdemeTarixDetailAPIView.as_view()),

    path('gifts/', contract_views.MuqavileHediyyeListCreateAPIView.as_view()),
    path('gifts/<int:pk>/', contract_views.MuqavileHediyyeDetailAPIView.as_view()),

    path('demo/', contract_views.DemoSatisListAPIView.as_view()),
    path('demo/<int:pk>/', contract_views.DemoSatisDetailAPIView.as_view()),
]
