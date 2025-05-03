import csv

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.forms import widgets
from django.http import HttpResponse, JsonResponse
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, View, FormView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib import messages
from apps.finance.models import Invoice
from .forms import ClassAssignmentNProjectForm
from .models import Student, ClassAssignmentNProject
from apps.result.utils import PermissionRequiredMessageMixin
import logging
logger = logging.getLogger()
# from datetime import timezone, timedelta
from django.utils import timezone
from django.contrib.auth.models import User, Group


class AssignmentListView(LoginRequiredMixin,PermissionRequiredMessageMixin, ListView):
    model = ClassAssignmentNProject
    context_object_name = "assignments"
    permission_required = 'students.view_student' 
    template_name = "project_n_assignments/assignment_list.html"


class AssignmentCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = ClassAssignmentNProject
    fields = ['name','file','for_class','is_assignment_for_all','students']
    success_message = "New student successfully added."
    permission_required = 'students.add_student'
    success_url = reverse_lazy('view-assignments')

    def form_valid(self, form):
        form.instance.user = self.request.user
        if form.cleaned_data.get('is_assignment_for_all'):
            form.instance.save()
            form.instance.students.set([])  # Clear students if it's for all
        return super().form_valid(form)

class AssignmentUpdateView(LoginRequiredMixin, PermissionRequiredMessageMixin, UpdateView):
    model = ClassAssignmentNProject
    fields = ['name','file','for_class','is_assignment_for_all','students','is_active']
    success_message = 'Assignment updated successfully.'
    permission_required = 'student.add_student'
    success_url = reverse_lazy('view-assignments')

class AssignmentDeleteView(LoginRequiredMixin,PermissionRequiredMessageMixin, DeleteView):
    permission_required = 'students.delete_student' 
    model = ClassAssignmentNProject
    success_url = reverse_lazy("view-assignments")


class LoadStudentsView(View):
    def get(self, request):
        class_id = request.GET.get('class_id')
        students = Student.objects.filter(current_class=class_id).values('id', 'firstname', 'surname','registration_number')
        student_list = [{"id": s["id"], "name": f'{s["firstname"]} {s["surname"]} - ({s["registration_number"]})'} for s in students]
        return JsonResponse({"students": student_list})