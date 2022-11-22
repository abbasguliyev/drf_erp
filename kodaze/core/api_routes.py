from django.conf import settings
from django.urls import include, path

from holiday.api import views as holiday_views
from statistika import statistika

from django.conf.urls.static import static

urlpatterns = [
    path('users/', include("account.api.urls")),
    path('company/', include("company.api.urls")),
    path('contract/', include("contract.api.urls")),
    path('backup/', include("backup_restore.api.urls")),
    path('update/', include("update.api.urls")),
    path('task-manager/', include("task_manager.api.urls")),
    path('product/', include("product.api.urls")),
    path('warehouse/', include("warehouse.api.urls")),
    path('salaries/', include("salary.api.urls")),
    path('cashbox/', include("cashbox.api.urls")),
    path('services/', include("services.api.urls")),
    path('transfer/', include("transfer.api.urls")),


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
