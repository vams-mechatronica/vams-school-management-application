from django.urls import path

from .views import *

urlpatterns = [
   path('students',StudentAttendanceView.as_view(),name="students-attendance"),
   path('students/add/',StudentAttendanceCreateView.as_view(),name="students-attendance-add"),
   path('get_students/<int:class_id>/', GetStudentsAPIView.as_view(), name='get_students'),
]
