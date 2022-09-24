from django.urls import path
from restAPI.v1.company import views as company_views

urlpatterns = [
    path('holding/', company_views.HoldingListCreateAPIView.as_view()),
    path('holding/<int:pk>/', company_views.HoldingDetailAPIView.as_view()),

    path('', company_views.ShirketListCreateAPIView.as_view()),
    path('<int:pk>/', company_views.ShirketDetailAPIView.as_view()),

    path('offices/', company_views.OfisListCreateAPIView.as_view()),
    path('offices/<int:pk>/', company_views.OfisDetailAPIView.as_view()),

    path('departments/', company_views.DepartmentListCreateAPIView.as_view()),
    path('departments/<int:pk>/', company_views.DepartmentDetailAPIView.as_view()),

    path('sections/', company_views.ShobeListCreateAPIView.as_view()),
    path('sections/<int:pk>/', company_views.ShobeDetailAPIView.as_view()),

    path('teams/', company_views.KomandaListCreateAPIView.as_view()),
    path('teams/<int:pk>/', company_views.KomandaDetailAPIView.as_view()),

    path('positions/', company_views.VezifelerListCreateAPIView.as_view()),
    path('positions/<int:pk>/', company_views.VezifelerDetailAPIView.as_view()),

    path('logo/', company_views.AppLogoListCreateAPIView.as_view()),
    path('logo/<int:pk>/', company_views.AppLogoDetailAPIView.as_view()),

    path('position-permissions/', company_views.VezifePermissionListCreateAPIView.as_view()),
    path('position-permissions/<int:pk>/', company_views.VezifePermissionDetailAPIView.as_view()),
]