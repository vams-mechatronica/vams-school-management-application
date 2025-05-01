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