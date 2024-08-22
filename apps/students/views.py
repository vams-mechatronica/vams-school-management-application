import csv

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.forms import widgets
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, View
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from apps.finance.models import Invoice

from .models import Student, StudentBulkUpload
from apps.result.utils import PermissionRequiredMessageMixin
import logging
logger = logging.getLogger()


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
        context = super(StudentDetailView, self).get_context_data(**kwargs)
        logger.info(context)
        context["payments"] = Invoice.objects.filter(student=self.object)
        return context

class StudentCreateView(LoginRequiredMixin,PermissionRequiredMessageMixin, SuccessMessageMixin, CreateView):
    model = Student
    fields = ['current_status','registration_number','surname','firstname','other_name','father_name','mother_name','gender','date_of_birth','date_of_admission','current_class','parent_mobile_number','address','others','adharcard_number','adharcard']
    success_message = "New student successfully added."
    permission_required = 'students.add_student' 

    def get_form(self):
        """add date picker in forms"""
        form = super(StudentCreateView, self).get_form()
        form.fields["date_of_birth"].widget = widgets.DateInput(attrs={"type": "date"})
        form.fields["date_of_admission"].widget = widgets.DateInput(attrs={"type": "date"})
        form.fields["address"].widget = widgets.Textarea(attrs={"rows": 2})
        form.fields["others"].widget = widgets.Textarea(attrs={"rows": 2})
        return form


class StudentUpdateView(LoginRequiredMixin, SuccessMessageMixin,PermissionRequiredMessageMixin, UpdateView):
    model = Student
    fields = "__all__"
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



class DownloadCSVViewdownloadcsv(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="student_template.csv"'

        writer = csv.writer(response)
        writer.writerow(
            [
                "registration_number",
                "surname",
                "firstname",
                "other_names",
                "gender",
                "parent_number",
                "address",
                "current_class",
            ]
        )

        return response
