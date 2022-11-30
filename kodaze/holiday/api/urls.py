from django.urls import path
from holiday.api import views as holiday_views

urlpatterns = [
    # holiday
    path('employee-working-days/', holiday_views.EmployeeWorkingDayListAPIView.as_view()),
    path('employee-holiday/', holiday_views.EmployeeHolidayListAPIView.as_view()),
    path('employee-holiday-history/', holiday_views.EmployeeHolidayHistoryListAPIView.as_view()),
    path('employee-holiday-history/<int:pk>/', holiday_views.EmployeeHolidayHistoryDetailAPIView.as_view()),
    path('holiday-operation/', holiday_views.HolidayOperationListCreateAPIView.as_view()),
    # day off
    path('employee-day-off/', holiday_views.EmployeeDayOffListAPIView.as_view()),
    path('employee-day-off-history/', holiday_views.EmployeeDayOffHistoryListAPIView.as_view()),
    path('employee-day-off-history/<int:pk>/', holiday_views.EmployeeDayOffHistoryDetailAPIView.as_view()),
    path('employee-day-off-operation/', holiday_views.EmployeeDayOffOperationListCreateAPIView.as_view()),
]