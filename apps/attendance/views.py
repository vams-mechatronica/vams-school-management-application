from django.shortcuts import render, redirect
from .models import Student, StudentAttendance
from apps.corecode.models import StudentClass
from django.utils import timezone
from django.http import JsonResponse
from django.core.paginator import Paginator

def attendance_form(request):
    if request.method == 'POST':
        date = request.POST['date-select']
        selected_class = request.POST['class']
        period = request.POST['period']
        
        students = Student.objects.filter(current_class=selected_class)
        for student in students:
            status = request.POST.get(f'status_{student.id}')
            remarks = request.POST.get(f'remarks_{student.id}')
            StudentAttendance.objects.create(
                student=student,
                date=date,
                status=status,
                remarks=remarks
            )
        return redirect('students-attendance')

    else:
        classes = StudentClass.objects.all()  # Assuming you have a Class model
        students = Student.objects.all()  # Empty queryset for initial load
        attendance_choices = StudentAttendance.ATTENDANCE_CHOICE

        context = {
            'classes': classes,
            'students': students,
            'attendance_choices': attendance_choices,
        }
        return render(request, 'attendance/students_attendance.html', context)

from django.http import JsonResponse
from django.core.paginator import Paginator
from django.utils.dateparse import parse_date
from .models import Student, StudentAttendance

def get_students(request, class_id):
    date_str = request.GET.get('date')
    period = request.GET.get('period')
    
    # Validate and parse the date
    date = parse_date(date_str) if date_str else None
    
    students = Student.objects.filter(current_class=class_id)

    if students.exists():
        paginator = Paginator(students, 10)  # Show 10 students per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    
    # Fetch attendance data only if date is provided
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
    
    students_list = [
        {'id': student.id, 'fullname': student.get_fullname(), **attendance_dict.get(student.id, {'status': None, 'remarks': ''})}
        for student in page_obj.object_list
    ]

    return JsonResponse({
        'students': students_list,
        'page': page_obj.number,
        'pages': paginator.num_pages,
    })