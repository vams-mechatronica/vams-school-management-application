from django.shortcuts import render, redirect
from .models import Student, StudentAttendance
from apps.corecode.models import StudentClass
from django.utils import timezone
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from django.shortcuts import redirect
from apps.result.utils import PermissionRequiredMessageMixin


class StudentAttendanceView(LoginRequiredMixin, PermissionRequiredMessageMixin, ListView):
    model = Student
    template_name = 'attendance/students_attendance.html'
    context_object_name = 'students'
    permission_required = 'attendance.view_studentattendance'

    def get_queryset(self):
        selected_class = self.request.GET.get('class', None)
        if selected_class:
            return Student.objects.filter(current_class=selected_class)
        return Student.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['classes'] = StudentClass.objects.all()
        context['attendance_choices'] = StudentAttendance.ATTENDANCE_CHOICE
        return context

class StudentAttendanceCreateView(LoginRequiredMixin, PermissionRequiredMessageMixin, CreateView):
    model = StudentAttendance
    fields = ['status', 'remarks']  # These fields are used by default; we'll override save method
    success_url = reverse_lazy('students-attendance')
    permission_required = 'attendance.add_studentattendance'

    def post(self, request, *args, **kwargs):
        date = request.POST['date-select']
        selected_class = request.POST['class']
        period = request.POST['period']

        students = Student.objects.filter(current_class=selected_class)
        for student in students:
            status = request.POST.get(f'status_{student.id}')
            remarks = request.POST.get(f'remarks_{student.id}')
            StudentAttendance.objects.update_or_create(
                student=student,
                date=date,
                defaults={
                    'status': status,
                    'remarks': remarks
                }
            )

        return redirect(self.success_url)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils.dateparse import parse_date
from .models import Student, StudentAttendance

class GetStudentsAPIView(APIView):

    def get(self, request, class_id):
        date_str = request.GET.get('date')
        period = request.GET.get('period')

        # Validate and parse the date
        date = parse_date(date_str) if date_str else None

        students = Student.objects.filter(current_class=class_id)

        attendance_data = {}
        if date:
            attendance_data = StudentAttendance.objects.filter(
                student__in=students,
                date=date
            ).values('student_id', 'status', 'remarks')
            
        attendance_dict = {
            item['student_id']: {'status': item['status'], 'remarks': item['remarks']}
            for item in attendance_data
        }

        if students.exists():
            students_list = [
                {
                    'id': student.id,
                    'fullname': student.get_fullname(),
                    **attendance_dict.get(student.id, {'status': None, 'remarks': ''})
                }
                for student in students
            ]

            return Response({
                'students': students_list,
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'students': [],
            }, status=status.HTTP_200_OK)


import calendar
import holidays
from django.db.models import Q
from datetime import date, timedelta
import pandas as pd
class AttendanceReportAPI(APIView):
    def get(self, request):
        class_id = request.GET.get('class')
        year = request.GET.get('year')
        if isinstance(year,str):
            year = int(year)
        month = request.GET.get('month')
        if isinstance(month,str):
            month = int(month)

        df = generate_attendance_report(class_id=class_id,year=year, month=month)
        return Response({'data':df.to_dict()},status=status.HTTP_200_OK)

def generate_attendance_report(class_id, year, month):
    try:
        class_obj = StudentClass.objects.get(id=class_id)
    except StudentClass.DoesNotExist:
        return "Please select a valid class"
    # Fetch students in the selected class
    students = Student.objects.filter(current_class=class_obj)

    # Get all dates in the month
    first_day = date(year, month, 1)
    last_day = date(year, month, calendar.monthrange(year, month)[1])
    date_range = [first_day + timedelta(days=i) for i in range((last_day - first_day).days + 1)]
    
    # Fetch attendance records for the given class and month
    attendance_records = StudentAttendance.objects.filter(
        student__in=students, date__range=(first_day, last_day)
    )

    # Fetch Indian holidays
    indian_holidays = holidays.India(years=year)

    # Prepare report dictionary
    report_data = []
    for student in students:
        row = {"Student": f"{student.firstname} {student.surname}"}
        for day in date_range:
            # Mark weekends (Saturday & Sunday in India)
            if day.weekday() in [6] or day in indian_holidays:
                row[day.strftime("%d-%b")] = "H"
                continue

            # Get attendance record for the student on this date
            attendance = attendance_records.filter(student=student, date=day).first()
            row[day.strftime("%d-%b")] = (
                "P" if attendance and attendance.status == "present" else
                "A" if attendance and attendance.status == "absent" else
                "L" if attendance and attendance.status == "on-leave" else
                "-"
            )
        
        report_data.append(row)
    
    # Convert to Pandas DataFrame for tabular display
    df = pd.DataFrame(report_data)
    return df


from datetime import datetime


def attendance_report_view(request):
    selected_class = 3
    year = datetime.now().year
    month = datetime.now().month
    report_data = []
    headers = []

    if request.method == "POST":
        selected_class = request.POST.get("class_id")
        year = int(request.POST.get("year"))
        month = int(request.POST.get("month"))
        # selected_class = StudentClass.objects.get(id=class_id)
        
    report_df = generate_attendance_report(selected_class, year, month)
    report_data = report_df.to_dict(orient="records")
    months = [(1, 'January'), (2, 'February'), (3, 'March'), (4, 'April'),
                                         (5, 'May'), (6, 'June'), (7, 'July'), (8, 'August'),
                                         (9, 'September'), (10, 'October'), (11, 'November'), (12, 'December')]
    headers = report_df.columns.tolist()
    classes = StudentClass.objects.all()
    return render(request, "attendance/student_attendance_report.html", {
        "classes": classes,
        "report_data": report_data,
        "headers": headers,
        "selected_class": selected_class,
        "year": year,
        "month": month,
        "select_month":months
    })
