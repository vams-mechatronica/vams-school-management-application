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
