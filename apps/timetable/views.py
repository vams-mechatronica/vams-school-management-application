from rest_framework import generics, permissions
from .models import Timetable, Student, Staff,Period,PeriodDay, StudentClass
from .serializers import TimetableSerializer
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from apps.result.utils import PermissionRequiredMessageMixin

from django.contrib.messages.views import SuccessMessageMixin
from django.forms import widgets
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, View
from django.views.generic.edit import CreateView, DeleteView, UpdateView

# Mapping day numbers to day names
DAY_MAPPING = {
    1: "Monday",
    2: "Tuesday",
    3: "Wednesday",
    4: "Thursday",
    5: "Friday",
    6: "Saturday"
}

class StudentTimetableView(generics.ListAPIView):
    serializer_class = TimetableSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        student = Student.objects.get(user=user)
        return Timetable.objects.filter(class_assigned=student.current_class)

class StaffTimetableView(generics.ListAPIView):
    serializer_class = TimetableSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        staff = Staff.objects.get(user=user)
        return Timetable.objects.filter(staff=staff)

class RequestModificationView(generics.CreateAPIView):
    serializer_class = TimetableSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()


from django.shortcuts import render, redirect
from .forms import TimetableForm

def add_timetable(request):
    if request.method == "POST":
        form = TimetableForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add-timetable')
    else:
        form = TimetableForm()
        timetables = Timetable.objects.all()
    return render(request, 'timetable/timetable_form.html', {'form': form,'timetable_records':timetables})


class TimetableDeleteView(LoginRequiredMixin,PermissionRequiredMessageMixin, DeleteView):
    permission_required = 'timetable.delete_timetable' 
    model = Timetable
    success_url = reverse_lazy("add-timetable")

class TimeTableUpdateView(LoginRequiredMixin, PermissionRequiredMessageMixin,UpdateView):
    permission_required = 'timetable.update_timetable'
    model = Timetable
    fields = '__all__'
    success_message = "Record successfully updated"
    success_url = reverse_lazy('add-timetable')

@login_required(login_url="login")
def timetable_view(request):
    user = request.user
    periods = list(Period.objects.all())  # Fetch periods as a list
    class_timetable = {}

    if user.is_superuser:
        # Admin: Show timetable for all classes
        classes = StudentClass.objects.all()
    elif user.groups.filter(name="Staff").exists():
        # Staff: Show only their own timetable if they have permission
        if user.has_perm("timetable.view_timetable"):  # Replace "app" with your app name
            classes = StudentClass.objects.filter(staff_assigned=user)
        else:
            classes = []
    elif user.groups.filter(name="Student").exists():
        # Student: Show only their class timetable
        student = getattr(user, "student", None)
        if student and student.current_class:
            classes = [student.current_class]
        else:
            classes = []
    else:
        classes = []
    
    for student_class in classes:
        days = {DAY_MAPPING[day['day']]: [None] * len(periods) for day in PeriodDay.objects.values('day')}
        timetables = Timetable.objects.filter(class_assigned=student_class)

        for entry in timetables:
            day_name = DAY_MAPPING.get(entry.day, "Unknown")
            period_index = next((i for i, p in enumerate(periods) if p == entry.period), None)

            if period_index is not None:
                days[day_name][period_index] = {
                    "period": entry.period.id,
                    "subject": entry.subject.name,
                    "teacher": f"{entry.staff.firstname} {entry.staff.surname}"
                }
        
        class_timetable[student_class.name] = days
    
    return render(request, "timetable/timetable.html", {
        "periods": periods,
        "class_timetable": class_timetable
    })
