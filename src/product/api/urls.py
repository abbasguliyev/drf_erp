from django.urls import path
from product.api import views as product_views

urlpatterns = [
    path('', product_views.ProductListCreateAPIView.as_view()),
    path('<int:pk>/', product_views.ProductDetailAPIView.as_view()),

    path('categories/', product_views.CategoryListCreateAPIView.as_view()),
    path('categories/<int:pk>/', product_views.CategoryDetailAPIView.as_view()),

    path('unit-of-measure/', product_views.UnitOfMeasureListCreateAPIView.as_view()),
    path('unit-of-measure/<int:pk>/', product_views.UnitOfMeasureDetailAPIView.as_view()),
    
    path('calculate-product-total-price/', product_views.calculate_products_total_price_view),
]