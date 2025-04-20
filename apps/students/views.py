import csv

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.forms import widgets
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, View, FormView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib import messages
from apps.finance.models import Invoice
from .forms import PromotionForm
from .models import Student, StudentBulkUpload
from apps.result.utils import PermissionRequiredMessageMixin
import logging
logger = logging.getLogger()
# from datetime import timezone, timedelta
from django.utils import timezone
from django.contrib.auth.models import User, Group
from apps.corecode.models import SchoolDetail


class StudentListView(LoginRequiredMixin,PermissionRequiredMessageMixin, ListView):
    model = Student
    context_object_name = "students"
    permission_required = 'students.view_student' 
    template_name = "students/student_list.html"

    def get_queryset(self):
        user = self.request.user

        # If the user is a superuser or staff, allow viewing all records
        if user.is_superuser or user.is_staff:
            return Student.objects.all()

        # If the user is in the 'Students' group, allow viewing only their own record
        if user.groups.filter(name='Students').exists():
            return Student.objects.filter(user=user)

        # Default: return an empty queryset if the user doesn't fit the above categories
        return Student.objects.none()



class StudentDetailView(LoginRequiredMixin, DetailView ,PermissionRequiredMessageMixin):
    model = Student
    template_name = "students/student_detail.html"
    permission_required = 'students.view_student' 

    def get_context_data(self, **kwargs):
        context = super(StudentDetailView, self).get_context_data(**kwargs)
        context["payments"] = Invoice.objects.filter(student=self.object)
        return context

class StudentDashboardView(LoginRequiredMixin, DetailView ,PermissionRequiredMessageMixin):
    model = Student
    template_name = "student_dashboard.html"
    permission_required = 'students.view_student' 

    def get_context_data(self, **kwargs):
        context = super(StudentDashboardView, self).get_context_data(**kwargs)
        logger.info(context)
        context["payments"] = Invoice.objects.filter(student=self.object)
        return context

class StudentCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Student
    fields = [
        'current_status', 'registration_number',  'firstname', 'other_name','surname',
        'father_name', 'mother_name', 'gender', 'date_of_birth', 'date_of_admission',
        'current_class', 
        'adharcard_number', 'adharcard','parent_mobile_number','email',
        'number_of_siblings','select_siblings', 'address', 'others',
        'uses_transport', 'route', 'pickup_drop_location', 'pickup_time', 'drop_time'
    ]
    success_message = "New student successfully added."
    permission_required = 'students.add_student'

    def get_form(self):
        form = super().get_form()
        form.fields["date_of_birth"].widget = widgets.DateInput(attrs={"type": "date"})
        form.fields["date_of_admission"].widget = widgets.DateInput(attrs={"type": "date"})
        form.fields["pickup_time"].widget = widgets.TimeInput(attrs={"type": "time"})
        form.fields["drop_time"].widget = widgets.TimeInput(attrs={"type": "time"})
        form.fields["address"].widget = widgets.Textarea(attrs={"rows": 2})
        form.fields["others"].widget = widgets.Textarea(attrs={"rows": 2})
        return form

    def get_registration_number(self):
        try:
            last_student = Student.objects.latest('updated_at')
            last_id = last_student.id
        except Student.DoesNotExist:
            import random
            last_id = random.randint(0, 99999)

        try:
            school_short_name = SchoolDetail.objects.latest('updated_at').short_name
        except SchoolDetail.DoesNotExist:
            school_short_name = "VAMS"

        timestamp = timezone.now().strftime('%d')
        reg_number = f"{school_short_name}/{timezone.now().year}/{timezone.now().month}/{timestamp}/{last_id + 1}"
        return reg_number

    def form_valid(self, form):
        student = form.instance

        firstname = student.firstname.strip().lower()
        lastname = student.surname.strip().lower()
        username = f"{lastname}.{firstname}"

        # Generate password
        dob_part = student.date_of_birth.strftime("%d%m")
        today_part = timezone.now().strftime("%d%m%Y")
        password = f"{dob_part}{firstname}{lastname}{today_part}#"

        # Create or get user
        user, created = User.objects.get_or_create(username=username, defaults={
            "first_name": student.firstname,
            "last_name": student.surname,
        })

        if created:
            user.set_password(password)
            user.save()

        # Assign to Student group
        student_group, _ = Group.objects.get_or_create(name="Student")
        user.groups.add(student_group)

        # Assign user and registration number to student
        student.user = user
        student.registration_number = self.get_registration_number()

        return super().form_valid(form)

class StudentUpdateView(LoginRequiredMixin, SuccessMessageMixin,PermissionRequiredMessageMixin, UpdateView):
    model = Student
    fields = [
        'current_status', 'registration_number',  'firstname', 'other_name','surname',
        'father_name', 'mother_name', 'gender', 'date_of_birth', 'date_of_admission',
        'current_class', 
        'adharcard_number', 'adharcard','parent_mobile_number','email',
        'number_of_siblings','select_siblings', 'address', 'others',
        'uses_transport', 'route', 'pickup_drop_location', 'pickup_time', 'drop_time'
    ]
    success_message = "Record successfully updated."
    permission_required = 'students.update_student' 


    def get_form(self):
        """add date picker in forms"""
        form = super(StudentUpdateView, self).get_form()
        form.fields["date_of_birth"].widget = widgets.DateInput(attrs={"type": "date"})
        form.fields["date_of_admission"].widget = widgets.DateInput(
            attrs={"type": "date"}
        )
        form.fields["address"].widget = widgets.Textarea(attrs={"rows": 2})
        form.fields["others"].widget = widgets.Textarea(attrs={"rows": 2})
        # form.fields['passport'].widget = widgets.FileInput()
        return form


class StudentDeleteView(LoginRequiredMixin,PermissionRequiredMessageMixin, DeleteView):
    permission_required = 'students.delete_student' 
    model = Student
    success_url = reverse_lazy("student-list")



class StudentBulkUploadView(LoginRequiredMixin, SuccessMessageMixin,PermissionRequiredMessageMixin, CreateView):
    model = StudentBulkUpload
    template_name = "students/students_upload.html"
    fields = ["csv_file"]
    success_url = "/student/list"
    permission_required = 'students.add_studentbulkupload' 
    success_message = "Successfully uploaded students"



class DownloadCSVView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="student_template.csv"'

        writer = csv.writer(response)
        
        # Define CSV Headers
        writer.writerow([
            "registration_number",  # Unique ID for student
            "student_name",         # Full name of the student
            "current_class",        # e.g., 5th, 10th
            "date_of_birth",        # YYYY-MM-DD
            "date_of_admission",    # YYYY-MM-DD
            "father_name",          # Father's full name
            "mother_name",          # Mother's full name
            "gender",               # Male/Female/Other
            "mobile_number",        # 10-digit phone number
            "email",                # Valid email address
            "address",              # Residential address
            "adharcard_number",     # 12-digit Aadhar number
        ])
        
        # Add a row with sample data for guidance
        writer.writerow([
            "REG12345",             # Sample registration number
            "John Doe",             # Sample student name
            "10th",                 # Class
            "2005-08-15",           # Date of birth
            "2020-06-12",           # Date of admission
            "Richard Doe",          # Father's name
            "Jane Doe",             # Mother's name
            "Male",                 # Gender
            "9876543210",           # Mobile number
            "john.doe@example.com", # Email
            "221B Baker Street",    # Address
            "123456789012",         # Aadhar number
        ])

        return response



class StudentPromotionView(PermissionRequiredMixin, FormView):
    template_name = 'students/promote_students.html'
    form_class = PromotionForm
    success_url = reverse_lazy('promote-students')
    permission_required = 'yourapp.can_promote_students'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        class_id = self.request.GET.get('current_class')
        if class_id:
            kwargs['class_id'] = class_id
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['selected_class'] = self.request.GET.get('current_class', '')
        return context
