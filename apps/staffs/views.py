from django.contrib.messages.views import SuccessMessageMixin
from django.forms import widgets
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from apps.result.utils import PermissionRequiredMessageMixin
from .models import Staff
from .forms import StaffForm


class StaffListView(ListView,PermissionRequiredMessageMixin):
    model = Staff
    permission_required = 'staffs.view_staff'


class StaffDetailView(DetailView,PermissionRequiredMessageMixin):
    model = Staff
    permission_required = 'staffs.view_staff'
    template_name = "staffs/staff_detail.html"



class StaffCreateView(SuccessMessageMixin, PermissionRequiredMessageMixin,CreateView):
    model = Staff
    form_class = StaffForm
    permission_required = "staffs.create_staff"
    success_message = "New staff successfully added"


class StaffUpdateView(SuccessMessageMixin,PermissionRequiredMessageMixin, UpdateView):
    model = Staff
    fields = "__all__"
    permission_required = "staffs.update_staff"
    success_message = "Record successfully updated."

    def get_form(self):
        """add date picker in forms"""
        form = super(StaffUpdateView, self).get_form()
        form.fields["date_of_birth"].widget = widgets.DateInput(attrs={"type": "date"})
        form.fields["date_of_admission"].widget = widgets.DateInput(
            attrs={"type": "date"}
        )
        form.fields["address"].widget = widgets.Textarea(attrs={"rows": 1})
        form.fields["others"].widget = widgets.Textarea(attrs={"rows": 1})
        return form


class StaffDeleteView(PermissionRequiredMessageMixin,DeleteView):
    model = Staff
    permission_required = "staffs.delete_staff"
    success_url = reverse_lazy("staff-list")
