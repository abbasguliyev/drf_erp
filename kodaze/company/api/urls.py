from django.urls import path
from company.api import views as company_views

urlpatterns = [
    path('holding/', company_views.HoldingListCreateAPIView.as_view()),
    path('holding/<int:pk>/', company_views.HoldingDetailAPIView.as_view()),

    path('', company_views.CompanyListCreateAPIView.as_view()),
    path('<int:pk>/', company_views.CompanyDetailAPIView.as_view()),

    path('offices/', company_views.OfficeListCreateAPIView.as_view()),
    path('offices/<int:pk>/', company_views.OfficeDetailAPIView.as_view()),

    path('departments/', company_views.DepartmentListCreateAPIView.as_view()),
    path('departments/<int:pk>/', company_views.DepartmentDetailAPIView.as_view()),

    path('sections/', company_views.SectionListCreateAPIView.as_view()),
    path('sections/<int:pk>/', company_views.SectionDetailAPIView.as_view()),

    path('teams/', company_views.TeamListCreateAPIView.as_view()),
    path('teams/<int:pk>/', company_views.TeamDetailAPIView.as_view()),

    path('positions/', company_views.PositionListCreateAPIView.as_view()),
    path('positions/<int:pk>/', company_views.PositionDetailAPIView.as_view()),

    path('logo/', company_views.AppLogoListCreateAPIView.as_view()),
    path('logo/<int:pk>/', company_views.AppLogoDetailAPIView.as_view()),

    path('position-permissions/', company_views.PermissionForPositionListCreateAPIView.as_view()),
    path('position-permissions/<int:pk>/', company_views.PermissionForPositionDetailAPIView.as_view()),
]