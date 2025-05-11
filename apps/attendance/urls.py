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
   path('ajax/calculate-days/', calculate_leave_days, name='calculate-leave-days'),

   path('leave-request/list/', LeaveRequestListView.as_view(), name='leave-list'),
   path('leave-request/new/', LeaveRequestCreateView.as_view(), name='leave-create'),
   path('leave-request/<int:pk>/approve/', LeaveApprovalView.as_view(), name='leave-approve'),
]
