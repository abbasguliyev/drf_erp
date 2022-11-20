from django.conf import settings
from django.urls import include, path

from api.v1.holiday import views as holiday_views
from api.v1.salary import views as salary_views
from api.v1.transfer import views as transfer_views
from api.v1.warehouse import views as warehouse_views
from api.v1.product import views as product_views
from api.v1.statistika import statistika

from rest_framework_simplejwt.views import token_refresh
from django.conf.urls.static import static

urlpatterns = [
    # account views *****************************************
    path('users/', include("api.v1.account.urls")),

    # company views *****************************************
    path('company/', include("api.v1.company.urls")),

    # contract views *****************************************
    path('contract/', include("api.v1.contract.urls")),

    # backup views *****************************************
    path('backup/', include("api.v1.backup_restore.urls")),

    # update views *****************************************
    path('update/', include("api.v1.update.urls")),

    # task manager url *****************************************
    path('task-manager/', include("api.v1.task_manager.urls")),

    # product_views *****************************************
    path('product/', include("api.v1.product.urls")),

    # warehouse_views *****************************************
    path('warehouse/', include("api.v1.warehouse.urls")),

    # salary views *****************************************
    path('salaries/', include("api.v1.salary.urls")),

    # cashbox views *****************************************
    path('cashbox/', include("api.v1.cashbox.urls")),

    # services views *****************************************
    path('services/', include("api.v1.services.urls")),

    # transfer views *****************************************
    path('transfer/', include("api.v1.transfer.urls")),


    # working_day views *****************************************
    path('holding-working_day/', holiday_views.HoldingWorkingDayListCreateAPIView.as_view()),
    path('holding-working_day/<int:pk>',
         holiday_views.HoldingWorkingDayDetailAPIView.as_view()),
    path('holding-istisna-employee/',
         holiday_views.HoldingExceptionWorkerListCreateAPIView.as_view()),
    path('holding-istisna-employee/<int:pk>',
         holiday_views.HoldingExceptionWorkerDetailAPIView.as_view()),

    path('company-working_day/', holiday_views.CompanyWorkingDayListCreateAPIView.as_view()),
    path('company-working_day/<int:pk>',
         holiday_views.CompanyWorkingDayDetailAPIView.as_view()),
    path('company-istisna-employee/',
         holiday_views.CompanyExceptionWorkerListCreateAPIView.as_view()),
    path('company-istisna-employee/<int:pk>',
         holiday_views.CompanyExceptionWorkerDetailAPIView.as_view()),

    path('office-working_day/', holiday_views.OfficeWorkingDayListCreateAPIView.as_view()),
    path('office-working_day/<int:pk>', holiday_views.OfficeWorkingDayDetailAPIView.as_view()),
    path('office-istisna-employee/',
         holiday_views.OfficeExceptionWorkerListCreateAPIView.as_view()),
    path('office-istisna-employee/<int:pk>',
         holiday_views.OfficeExceptionWorkerDetailAPIView.as_view()),

    path('section-working_day/', holiday_views.SectionWorkingDayListCreateAPIView.as_view()),
    path('section-working_day/<int:pk>', holiday_views.SectionWorkingDayDetailAPIView.as_view()),
    path('section-istisna-employee/',
         holiday_views.SectionExceptionWorkerListCreateAPIView.as_view()),
    path('section-istisna-employee/<int:pk>',
         holiday_views.SectionExceptionWorkerDetailAPIView.as_view()),

    path('team-working_day/', holiday_views.TeamWorkingDayListCreateAPIView.as_view()),
    path('team-working_day/<int:pk>',
         holiday_views.TeamWorkingDayDetailAPIView.as_view()),
    path('team-istisna-employee/',
         holiday_views.TeamExceptionWorkerListCreateAPIView.as_view()),
    path('team-istisna-employee/<int:pk>',
         holiday_views.TeamExceptionWorkerDetailAPIView.as_view()),

    path('position-working_day/', holiday_views.PositionWorkingDayListCreateAPIView.as_view()),
    path('position-working_day/<int:pk>',
         holiday_views.PositionWorkingDayDetailAPIView.as_view()),
    path('position-istisna-employee/',
         holiday_views.PositionExceptionWorkerListCreateAPIView.as_view()),
    path('position-istisna-employee/<int:pk>',
         holiday_views.PositionExceptionWorkerDetailAPIView.as_view()),

    path('employee-working_day/', holiday_views.EmployeeWorkingDayListCreateAPIView.as_view()),
    path('employee-working_day/<int:pk>', holiday_views.EmployeeWorkingDayDetailAPIView.as_view()),

    # statistika views *****************************************
    path('statistika/sale-quantityi', statistika.SalaryViewStatistikaAPIView.as_view(),
         name="sale_quantity_statistika"),
    path('statistika/demo-statistika',
         statistika.DemoStatistikaListAPIView.as_view(), name="demo_statistika"),
    path('statistika/contract-statistika',
         statistika.ContractStatistikaAPIView.as_view(), name="contract_statistika"),
    path('statistika/user-statistika',
         statistika.UserStatistikaList.as_view(), name="user_statistika"),
    path('statistika/service-statistika',
         statistika.ServiceStatistikaAPIView.as_view(), name="service_statistika"),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
