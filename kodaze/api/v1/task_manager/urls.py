from django.urls import path

from api.v1.task_manager import views as task_views

urlpatterns = [
    # task manager views *****************************************
    path('', task_views.TaskManagerListCreateAPIView.as_view()),
    path('<int:pk>/', task_views.TaskManagerDetailAPIView.as_view()),

    # task request views *****************************************
    path('task-request/', task_views.UserTaskRequestListCreateAPIView.as_view()),
    path('task-request/<int:pk>/', task_views.UserTaskRequestDetailAPIView.as_view()),

    # task manager views *****************************************
    path('advertisement/', task_views.AdvertisementListCreateAPIView.as_view()),
    path('advertisement/<int:pk>/', task_views.AdvertisementDetailAPIView.as_view()),
]