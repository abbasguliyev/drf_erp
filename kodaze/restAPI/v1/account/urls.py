from django.urls import path

from restAPI.v1.account import views as account_views

from rest_framework_simplejwt.views import token_refresh

urlpatterns = [
    path('', account_views.UserList.as_view()),
    path('<int:pk>/', account_views.UserDetail.as_view()),
    path('register/', account_views.RegisterApi.as_view()),
    path('permission-list/', account_views.PermissionListApi.as_view(),
         name="permission_list"),

    path('permission-group/', account_views.GroupCreateApi.as_view()),
    path('all-permission-group/', account_views.GroupListApi.as_view()),
    path('permission-group/<int:pk>/', account_views.GroupDetailApi.as_view()),

    path("login/", account_views.Login.as_view()),
    path("token-refresh/", token_refresh),
    path('change-password/', account_views.ChangePasswordView.as_view(),
         name='change_password'),
    path('password-reset/', account_views.ResetPasswordView.as_view(),
         name='password_reset'),

]