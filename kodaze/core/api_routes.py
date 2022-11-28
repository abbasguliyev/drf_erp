from django.conf import settings
from django.urls import include, path
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
    path('holidays/', include("holiday.api.urls")),

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
