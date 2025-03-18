from django.urls import path
from .views import StudentTimetableView,\
      StaffTimetableView, RequestModificationView,\
        add_timetable,timetable_view,TimetableDeleteView,\
            TimeTableUpdateView

urlpatterns = [
    path('view/', timetable_view, name='view-timetable'),
    path('add/',add_timetable,name="add-timetable"),
    path('update/<int:pk>/',TimeTableUpdateView.as_view(),name="update-timetable"),
    path('delete/<int:pk>/',TimetableDeleteView.as_view(),name="delete-timetable"),
    path('student/', StudentTimetableView.as_view(), name='student_timetable'),
    path('staff/', StaffTimetableView.as_view(), name='staff_timetable'),
    path('staff/request-modification/', RequestModificationView.as_view(), name='request_modification'),
]
