from django.urls import path
from restAPI.v1.salary import views as salary_views

urlpatterns = [
    path('salary-views/', salary_views.SalaryViewListCreateAPIView.as_view()),
    path('salary-views/<int:pk>/', salary_views.SalaryViewDetailAPIView.as_view()),

    path('bonus/', salary_views.BonusListCreateAPIView.as_view()),
    path('bonus/<int:pk>/', salary_views.BonusDetailAPIView.as_view()),

    path('pay-salary/', salary_views.PaySalaryListCreateAPIView.as_view()),
    path('pay-salary/<int:pk>/', salary_views.PaySalaryDetailAPIView.as_view()),

    path('advancepayment/', salary_views.AdvancePaymentListCreateAPIView.as_view()),
    path('advancepayment/<int:pk>/', salary_views.AdvancePaymentDetailAPIView.as_view()),

    path('salary-deduction/', salary_views.SalaryDeductionListCreateAPIView.as_view()),
    path('salary-deduction/<int:pk>/', salary_views.SalaryDeductionDetailAPIView.as_view()),

    path('office-leader-prim/',salary_views.OfficeLeaderPrimListCreateAPIView.as_view()),
    path('office-leader-prim/<int:pk>/', salary_views.OfficeLeaderPrimDetailAPIView.as_view()),

    path('group-leader-prim/', salary_views.GroupLeaderPrimNewListCreateAPIView.as_view()),
    path('group-leader-prim/<int:pk>/', salary_views.GroupLeaderPrimNewDetailAPIView.as_view()),

    path('manager2-prim/', salary_views.Manager2PrimListCreateAPIView.as_view()),
    path('manager2-prim/<int:pk>/', salary_views.Manager2PrimDetailAPIView.as_view()),

    path('manager1-prim/', salary_views.Manager1PrimNewListCreateAPIView.as_view()),
    path('manager1-prim/<int:pk>/', salary_views.Manager1PrimNewDetailAPIView.as_view()),

    path('creditor-prim/', salary_views.CreditorPrimListCreateAPIView.as_view()),
    path('creditor-prim/<int:pk>/', salary_views.CreditorPrimDetailAPIView.as_view()),

]