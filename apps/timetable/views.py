from rest_framework import generics, permissions
from .models import Timetable, Student, Staff,Period,PeriodDay, StudentClass
from .serializers import TimetableSerializer
from django.contrib.auth.models import User

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
            return redirect('add_timetable')
    else:
        form = TimetableForm()
        timetables = Timetable.objects.all()
    return render(request, 'timetable/timetable_form.html', {'form': form,'timetable_records':timetables})

def timetable_view(request):
    periods = list(Period.objects.all())  # Fetch periods as a list
    classes = StudentClass.objects.all()  # Fetch all classes
    
    class_timetable = {}

    for student_class in classes:
        # Create an empty timetable for each class
        days = {DAY_MAPPING[day['day']]: [None] * len(periods) for day in PeriodDay.objects.values('day')}
        
        timetables = Timetable.objects.filter(class_assigned=student_class)  # Filter timetable for the class

        # Populate timetable_data dictionary
        for entry in timetables:
            day_name = DAY_MAPPING.get(entry.day, "Unknown")  # Convert day number to name
            period_index = next((i for i, p in enumerate(periods) if p == entry.period), None)  # Get index of period

            if period_index is not None:
                days[day_name][period_index] = {
                    "period": entry.period.id,
                    "subject": entry.subject.name,  # Display period name
                    "teacher": f"{entry.staff.firstname} {entry.staff.surname}"  # Corrected teacher name
                }

        class_timetable[student_class.name] = days

    return render(request, "timetable/timetable.html", {
        "periods": periods,
        "class_timetable": class_timetable
    })
