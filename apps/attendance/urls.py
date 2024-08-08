from django.urls import path

from .views import *

urlpatterns = [
   path('students',attendance_form,name="students-attendance"),
   path('get_students/<int:class_id>/', get_students, name='get_students'),
]
