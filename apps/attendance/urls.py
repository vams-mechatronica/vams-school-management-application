from django.urls import path

from .views import *

urlpatterns = [
   path('students',StudentAttendanceView.as_view(),name="students-attendance"),
   path('students/add/',StudentAttendanceCreateView.as_view(),name="students-attendance-add"),
   path('get_students/<int:class_id>/', GetStudentsAPIView.as_view(), name='get_students'),
   path('generate-report',AttendanceReportAPI.as_view(),name="generate-attendance-report"),
   path('attendance-report-view',attendance_report_view,name="attendance-report-view"),
   path('staff-attendance/', bulk_attendance_view, name='staff-attendance'),
   path('staff-attendance-report/', MonthlyAttendanceReportView.as_view(), name='staff-attendance-report'),
]
