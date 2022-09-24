from django.conf import settings
from django.urls import include, path

from restAPI.v1.cashbox import views as cashbox_views
from restAPI.v1.holiday import views as holiday_views
from restAPI.v1.salary import views as salary_views
from restAPI.v1.services import views as services_views
from restAPI.v1.transfer import views as transfer_views
from restAPI.v1.warehouse import views as warehouse_views
from restAPI.v1.product import views as product_views
from restAPI.v1.income_expense import views as income_expense_views
from restAPI.v1.statistika import statistika

from rest_framework_simplejwt.views import token_refresh
from django.conf.urls.static import static

urlpatterns = [
    # account views *****************************************
    path('users/', include("restAPI.v1.account.urls")),

    # company views *****************************************
    path('company/', include("restAPI.v1.company.urls")),

    # muqavile views *****************************************
    path('contract/', include("restAPI.v1.contract.urls")),

    # backup views *****************************************
    path('backup/', include("restAPI.v1.backup_restore.urls")),

    # update views *****************************************
    path('update/', include("restAPI.v1.update.urls")),

    # task manager url *****************************************
    path('task-manager/', include("restAPI.v1.task_manager.urls")),

    # maas views *****************************************
    path('maas-goruntuleme/', salary_views.MaasGoruntulemeListCreateAPIView.as_view(),
         name="maas_goruntuleme"),
    path('maas-goruntuleme/<int:pk>', salary_views.MaasGoruntulemeDetailAPIView.as_view(),
         name="maas_goruntuleme_detail"),

    path('bonus/', salary_views.BonusListCreateAPIView.as_view(), name="bonus"),
    path('bonus/<int:pk>', salary_views.BonusDetailAPIView.as_view(),
         name="bonus_detail"),

    path('maas-ode/', salary_views.MaasOdeListCreateAPIView.as_view()),
    path('maas-ode/<int:pk>', salary_views.MaasOdeDetailAPIView.as_view()),

    path('avans/', salary_views.AvansListCreateAPIView.as_view(), name="avans"),
    path('avans/<int:pk>', salary_views.AvansDetailAPIView.as_view(),
         name="avans_detail"),

    path('kesinti/', salary_views.KesintiListCreateAPIView.as_view(), name="kesinti"),
    path('kesinti/<int:pk>', salary_views.KesintiDetailAPIView.as_view(),
         name="kesinti_detail"),

    path('office-leader-prim/',
         salary_views.OfficeLeaderPrimListCreateAPIView.as_view()),
    path('office-leader-prim/<int:pk>',
         salary_views.OfficeLeaderPrimDetailAPIView.as_view()),

    path('vanleader-prim/', salary_views.GroupLeaderPrimNewListCreateAPIView.as_view()),
    path('vanleader-prim/<int:pk>',
         salary_views.GroupLeaderPrimNewDetailAPIView.as_view()),

    path('canvasser-prim/', salary_views.Menecer2PrimListCreateAPIView.as_view()),
    path('canvasser-prim/<int:pk>',
         salary_views.Menecer2PrimDetailAPIView.as_view()),

    path('dealer-prim/', salary_views.Menecer1PrimNewListCreateAPIView.as_view()),
    path('dealer-prim/<int:pk>', salary_views.Menecer1PrimNewDetailAPIView.as_view()),

    path('kreditor-prim/', salary_views.KreditorPrimListCreateAPIView.as_view()),
    path('kreditor-prim/<int:pk>', salary_views.KreditorPrimDetailAPIView.as_view()),

    # gunler views *****************************************
    path('holding-gunler/', holiday_views.HoldingGunlerListCreateAPIView.as_view()),
    path('holding-gunler/<int:pk>',
         holiday_views.HoldingGunlerDetailAPIView.as_view()),
    path('holding-istisna-isci/',
         holiday_views.HoldingIstisnaIsciListCreateAPIView.as_view()),
    path('holding-istisna-isci/<int:pk>',
         holiday_views.HoldingIstisnaIsciDetailAPIView.as_view()),

    path('shirket-gunler/', holiday_views.ShirketGunlerListCreateAPIView.as_view()),
    path('shirket-gunler/<int:pk>',
         holiday_views.ShirketGunlerDetailAPIView.as_view()),
    path('shirket-istisna-isci/',
         holiday_views.ShirketIstisnaIsciListCreateAPIView.as_view()),
    path('shirket-istisna-isci/<int:pk>',
         holiday_views.ShirketIstisnaIsciDetailAPIView.as_view()),

    path('ofis-gunler/', holiday_views.OfisGunlerListCreateAPIView.as_view()),
    path('ofis-gunler/<int:pk>', holiday_views.OfisGunlerDetailAPIView.as_view()),
    path('ofis-istisna-isci/',
         holiday_views.OfisIstisnaIsciListCreateAPIView.as_view()),
    path('ofis-istisna-isci/<int:pk>',
         holiday_views.OfisIstisnaIsciDetailAPIView.as_view()),

    path('shobe-gunler/', holiday_views.ShobeGunlerListCreateAPIView.as_view()),
    path('shobe-gunler/<int:pk>', holiday_views.ShobeGunlerDetailAPIView.as_view()),
    path('shobe-istisna-isci/',
         holiday_views.ShobeIstisnaIsciListCreateAPIView.as_view()),
    path('shobe-istisna-isci/<int:pk>',
         holiday_views.ShobeIstisnaIsciDetailAPIView.as_view()),

    path('komanda-gunler/', holiday_views.KomandaGunlerListCreateAPIView.as_view()),
    path('komanda-gunler/<int:pk>',
         holiday_views.KomandaGunlerDetailAPIView.as_view()),
    path('komanda-istisna-isci/',
         holiday_views.KomandaIstisnaIsciListCreateAPIView.as_view()),
    path('komanda-istisna-isci/<int:pk>',
         holiday_views.KomandaIstisnaIsciDetailAPIView.as_view()),

    path('vezife-gunler/', holiday_views.VezifeGunlerListCreateAPIView.as_view()),
    path('vezife-gunler/<int:pk>',
         holiday_views.VezifeGunlerDetailAPIView.as_view()),
    path('vezife-istisna-isci/',
         holiday_views.VezifeIstisnaIsciListCreateAPIView.as_view()),
    path('vezife-istisna-isci/<int:pk>',
         holiday_views.VezifeIstisnaIsciDetailAPIView.as_view()),

    path('isci-gunler/', holiday_views.IsciGunlerListCreateAPIView.as_view()),
    path('isci-gunler/<int:pk>', holiday_views.IsciGunlerDetailAPIView.as_view()),

    path('isci-gelib-getme-vaxtlari/',
         holiday_views.IsciGelibGetmeVaxtlariListCreateAPIView.as_view()),
    path('isci-gelib-getme-vaxtlari/<int:pk>',
         holiday_views.IsciGelibGetmeVaxtlariDetailAPIView.as_view()),

    # cashbox views *****************************************
    path('pul-axini/', cashbox_views.PulAxiniListAPIView.as_view(), name="pul_axini"),
    path('pul-axini/<int:pk>', cashbox_views.PulAxiniDetailAPIView.as_view(),
         name="pul_axini_detail"),

    path('holding-kassa/', cashbox_views.HoldingKassaListCreateAPIView.as_view(),
         name="holding_kassa"),
    path('holding-kassa/<int:pk>', cashbox_views.HoldingKassaDetailAPIView.as_view(),
         name="holding_kassa_detail"),

    path('shirket-kassa/', cashbox_views.ShirketKassaListCreateAPIView.as_view(),
         name="shirket_kassa"),
    path('shirket-kassa/<int:pk>', cashbox_views.ShirketKassaDetailAPIView.as_view(),
         name="shirket_kassa_detail"),

    path('ofis-kassa/', cashbox_views.OfisKassaListCreateAPIView.as_view(),
         name="ofis_kassa"),
    path('ofis-kassa/<int:pk>', cashbox_views.OfisKassaDetailAPIView.as_view(),
         name="ofis_kassa_detail"),

    # transfer_views ***************************************
    path('shirket-holding-transfer/', transfer_views.ShirketdenHoldingeTransferListCreateAPIView.as_view(),
         name="shirket_holding_transfer"),
    path('shirket-holding-transfer/<int:pk>', transfer_views.ShirketdenHoldingeTransferDetailAPIView.as_view(),
         name="shirket_holding_transfer_detail"),

    path('holding-shirket-transfer/', transfer_views.HoldingdenShirketlereTransferListCreateAPIView.as_view(),
         name="holding_shirket_transfer"),
    path('holding-shirket-transfer/<int:pk>', transfer_views.HoldingdenShirketlereTransferDetailAPIView.as_view(),
         name="holding_shirket_transfer_detail"),

    path('shirket-ofis-transfer/', transfer_views.ShirketdenOfislereTransferListCreateAPIView.as_view(),
         name="shirket_ofis_transfer"),
    path('shirket-ofis-transfer/<int:pk>', transfer_views.ShirketdenOfislereTransferDetailAPIView.as_view(),
         name="shirket_ofis_transfer_detail"),

    path('ofis-shirket-transfer/', transfer_views.OfisdenShirketeTransferListCreateAPIView.as_view(),
         name="ofis_shirket_transfer"),
    path('ofis-shirket-transfer/<int:pk>', transfer_views.OfisdenShirketeTransferDetailAPIView.as_view(),
         name="ofis_shirket_transfer_detail"),

    # income_expense_views *********************************
    path('holding-kassa-medaxil/', income_expense_views.HoldingKassaMedaxilListCreateAPIView.as_view(),
         name="holding_kassa_medaxil"),
    path('holding-kassa-medaxil/<int:pk>', income_expense_views.HoldingKassaMedaxilDetailAPIView.as_view(),
         name="holding_kassa_medaxil_detail"),

    path('holding-kassa-mexaric/', income_expense_views.HoldingKassaMexaricListCreateAPIView.as_view(),
         name="holding_kassa_mexaric"),
    path('holding-kassa-mexaric/<int:pk>', income_expense_views.HoldingKassaMexaricDetailAPIView.as_view(),
         name="holding_kassa_mexaric_detail"),

    path('shirket-kassa-medaxil/', income_expense_views.ShirketKassaMedaxilListCreateAPIView.as_view(),
         name="shirket_kassa_medaxil"),
    path('shirket-kassa-medaxil/<int:pk>', income_expense_views.ShirketKassaMedaxilDetailAPIView.as_view(),
         name="shirket_kassa_medaxil_detail"),

    path('shirket-kassa-mexaric/', income_expense_views.ShirketKassaMexaricListCreateAPIView.as_view(),
         name="shirket_kassa_mexaric"),
    path('shirket-kassa-mexaric/<int:pk>', income_expense_views.ShirketKassaMexaricDetailAPIView.as_view(),
         name="shirket_kassa_mexaric_detail"),

    path('ofis-kassa-medaxil/', income_expense_views.OfisKassaMedaxilListCreateAPIView.as_view(),
         name="ofis_kassa_medaxil"),
    path('ofis-kassa-medaxil/<int:pk>', income_expense_views.OfisKassaMedaxilDetailAPIView.as_view(),
         name="ofis_kassa_medaxil_detail"),

    path('ofis-kassa-mexaric/', income_expense_views.OfisKassaMexaricListCreateAPIView.as_view(),
         name="ofis_kassa_mexaric"),
    path('ofis-kassa-mexaric/<int:pk>', income_expense_views.OfisKassaMexaricDetailAPIView.as_view(),
         name="ofis_kassa_mexaric_detail"),

    # product_views *****************************************
    path('mehsullar/', product_views.MehsullarListCreateAPIView.as_view(),
         name="mehsullar"),
    path('mehsullar/<int:pk>', product_views.MehsullarDetailAPIView.as_view(),
         name="mehsullar_detail"),

    # warehouse_views *****************************************
    path('anbar/', warehouse_views.AnbarListCreateAPIView.as_view(), name="anbar"),
    path('anbar/<int:pk>', warehouse_views.AnbarDetailAPIView.as_view(),
         name="anbar_detail"),

    path('anbar-qeydler/', warehouse_views.AnbarQeydlerListCreateAPIView.as_view(),
         name="anbar_qeydler"),
    path('anbar-qeydler/<int:pk>', warehouse_views.AnbarQeydlerDetailAPIView.as_view(),
         name="anbar_qeydler_detail"),

    path('emeliyyat/', warehouse_views.EmeliyyatListCreateAPIView.as_view(),
         name="emeliyyat"),
    path('emeliyyat/<int:pk>', warehouse_views.EmeliyyatDetailAPIView.as_view(),
         name="emeliyyat_detail"),

    path('stok/', warehouse_views.StokListCreateAPIView.as_view(), name="stok"),
    path('stok/<int:pk>', warehouse_views.StokDetailAPIView.as_view(),
         name="stok_detail"),

    # services_views *****************************************
    path('servis/', services_views.ServisListCreateAPIView.as_view(), name="servis"),
    path('servis/<int:pk>', services_views.ServisDetailAPIView.as_view(),
         name="servis_detail"),

    path('servis-odeme/', services_views.ServisOdemeListCreateAPIView.as_view()),
    path('servis-odeme/<int:pk>', services_views.ServisOdemeDetailAPIView.as_view()),

    # statistika views *****************************************
    path('statistika/satis-sayi', statistika.MaasGoruntulemeStatistikaAPIView.as_view(),
         name="satis_sayi_statistika"),
    path('statistika/demo-statistika',
         statistika.DemoStatistikaListAPIView.as_view(), name="demo_statistika"),
    path('statistika/muqavile-statistika',
         statistika.MuqavileStatistikaAPIView.as_view(), name="muqavile_statistika"),
    path('statistika/user-statistika',
         statistika.UserStatistikaList.as_view(), name="user_statistika"),
    path('statistika/servis-statistika',
         statistika.ServisStatistikaAPIView.as_view(), name="servis_statistika"),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
