from django.shortcuts import render, redirect
from .models import Student, StudentAttendance, Staff,StaffAttendance
from apps.corecode.models import StudentClass
from django.utils import timezone
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, View
from django.shortcuts import redirect
from .forms import BulkAttendanceForm
import logging
from apps.result.utils import PermissionRequiredMessageMixin
from django.db.models import Sum, F, ExpressionWrapper, fields

logger = logging.getLogger(__name__)


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

class StudentAttendanceCreateView(LoginRequiredMixin, PermissionRequiredMessageMixin,SuccessMessageMixin, CreateView):
    model = StudentAttendance
    fields = ['status', 'remarks']
    success_url = reverse_lazy('students-attendance')
    success_message = "Attendance added successfully"
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
        # messages.success(request,'Attendance updated successfully')
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
        try:
            class_obj = StudentClass.objects.get(id=class_id)
        except StudentClass.DoesNotExist:
            return Response({'error':'Enter a valid class'},status=status.HTTP_400_BAD_REQUEST)
        df = generate_attendance_report(class_id=class_id,year=year, month=month)
        return Response({'data':df.to_dict()},status=status.HTTP_200_OK)

def generate_attendance_report(class_id, year, month):
    try:
        class_obj = StudentClass.objects.get(id=class_id)
    except StudentClass.DoesNotExist:

        pass
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
            if day.weekday() in [6]:
                row[day.strftime("%d-%b")] = "Sunday"
                continue
            elif day in indian_holidays:
                row[day.strftime("%d-%b")] = "Holiday"
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
    selected_class = None
    year = datetime.now().year
    month = datetime.now().month
    report_data = []
    headers = []

    if request.method == "POST":
        selected_class = request.POST.get("class_id")
        year = int(request.POST.get("year"))
        month = int(request.POST.get("month"))
        # selected_class = StudentClass.objects.get(id=class_id)
    if selected_class:
        report_df = generate_attendance_report(selected_class, year, month)
        report_data = report_df.to_dict(orient="records")
        headers = report_df.columns.tolist()
    else:
        report_data = pd.DataFrame().to_dict(orient='records')
    months = [(1, 'January'), (2, 'February'), (3, 'March'), (4, 'April'),
                                        (5, 'May'), (6, 'June'), (7, 'July'), (8, 'August'),
                                        (9, 'September'), (10, 'October'), (11, 'November'), (12, 'December')]
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


def bulk_attendance_view(request):
    staff_list = Staff.objects.all()  # Fetch all staff
    attendance_records = {int(a.staff.id): a for a in StaffAttendance.objects.filter(date=datetime.now().date())}

    if request.method == "POST":
        form = BulkAttendanceForm(request.POST)
        if form.is_valid():
            attendance_date = form.cleaned_data['date']

            for staff in staff_list:
                status = request.POST.get(f'attendance_{staff.id}', '0')  # Default to Absent
                time_in = request.POST.get(f'check_in_{staff.id}') or None
                time_out = request.POST.get(f'check_out_{staff.id}') or None

                StaffAttendance.objects.update_or_create(
                    staff=staff,
                    date=attendance_date,
                    defaults={'status': status, 'time_in': time_in, 'time_out': time_out}
                )

            return redirect('staff-attendance')

    else:
        form = BulkAttendanceForm()

    return render(request, 'attendance/staff_attendance_bulk.html', {
        'form': form,
        'staff_list': staff_list,
        'attendance_records': attendance_records  # Pass the dictionary correctly
    })

def get_holidays():
    # Placeholder function to fetch holidays (this should be replaced with actual holiday fetching logic)
    return {datetime.now().date(): "Holiday"}  # Example: Dictionary with holiday dates

import holidays
from datetime import datetime, timedelta

class MonthlyAttendanceReportView(LoginRequiredMixin, PermissionRequiredMessageMixin, SuccessMessageMixin, View):
    permission_required = "attendance.view_staffattendance"

    def get(self, request):
        try:
            month = request.GET.get('month', datetime.now().strftime('%Y-%m'))
            start_date = datetime.strptime(month, '%Y-%m').date().replace(day=1)
            end_date = (start_date + timedelta(days=32)).replace(day=1) - timedelta(days=1)

            # Generate list of dates
            date_list = [start_date + timedelta(days=i) for i in range((end_date - start_date).days + 1)]
            date_range = [date.strftime('%d/%m') for date in date_list]

            # Get Indian holidays
            india_holidays = holidays.India(years=start_date.year)

            # Get all staff members
            staff_list = Staff.objects.all()

            # Fetch attendance data
            attendance_records = StaffAttendance.objects.filter(
                date__range=[start_date, end_date],
                status=1, time_in__isnull=False, time_out__isnull=False
            ).annotate(
                hours_spent=ExpressionWrapper(
                    F('time_out') - F('time_in'),
                    output_field=fields.DurationField()
                )
            ).values('staff__id', 'staff__firstname', 'staff__surname', 'date').annotate(
                total_hours=Sum('hours_spent')
            )

            # Process attendance data
            attendance_data = {}
            for record in attendance_records:
                staff_id = record['staff__id']
                date_str = record['date'].strftime('%d/%m')
                total_seconds = record['total_hours'].total_seconds()
                hours = int(total_seconds // 3600)
                minutes = int((total_seconds % 3600) // 60)
                formatted_hours = f"{hours}h {minutes}m"

                if staff_id not in attendance_data:
                    attendance_data[staff_id] = {}
                attendance_data[staff_id][date_str] = formatted_hours
        
            for staff in staff_list:
                staff_id = staff.id
                if staff_id not in attendance_data:
                    attendance_data[staff_id] = {}
                for date_str in date_range:
                    if date_str not in attendance_data[staff_id]:
                        day = datetime.strptime(f"{date_str}/{start_date.year}", "%d/%m/%Y").date() 
                        if day.weekday() == 6:  # Sunday
                            attendance_data[staff_id][date_str] = "Sunday"
                        elif day in india_holidays:
                            attendance_data[staff_id][date_str] = "Holiday"
                        else:
                            attendance_data[staff_id][date_str] = "-"

        except Exception as e:
            logger.exception(e)
            attendance_data = {}
            date_range = []
            staff_list = []

        report_available = bool(attendance_data)

        return render(request, 'attendance/staff_attendance_report.html', {
            'month': month,
            'date_range': date_range,
            'staff_list': staff_list,
            'attendance_data': attendance_data,
            'report_available': report_available
        })


def api_monthly_attendance_report(request):
    month = request.GET.get('month', datetime.now().strftime('%Y-%m'))
    start_date = datetime.strptime(month, '%Y-%m').date().replace(day=1)
    end_date = (start_date + timedelta(days=32)).replace(day=1) - timedelta(days=1)
    
    holidays = get_holidays()
    
    attendance_data = StaffAttendance.objects.filter(date__range=[start_date, end_date], status=1, time_in__isnull=False, time_out__isnull=False)
    
    attendance_data = attendance_data.annotate(
        hours_spent=ExpressionWrapper(
            F('time_out') - F('time_in'),
            output_field=fields.DurationField()
        )
    ).values('staff__firstname', 'staff__surname', 'date').annotate(
        total_hours=Sum('hours_spent')
    ).order_by('date')
    
    # Format hours_spent to only show hours and minutes
    for record in attendance_data:
        total_seconds = record['total_hours'].total_seconds()
        hours = int(total_seconds // 3600)
        minutes = int((total_seconds % 3600) // 60)
        record['total_hours'] = f"{hours}h {minutes}m"
    
    return JsonResponse({'attendance_data': list(attendance_data), 'holidays': holidays})
