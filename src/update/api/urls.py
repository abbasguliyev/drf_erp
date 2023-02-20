from django.urls import path
from update.api import views as update_views

urlpatterns = [
    path('', update_views.UpdateListCreateAPIView.as_view()),
    path('<int:pk>/', update_views.UpdateDetailAPIView.as_view()),
]