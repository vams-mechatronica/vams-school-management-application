from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.forms import widgets
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages

import csv
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView,View
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from apps.result.utils import PermissionRequiredMessageMixin
from .models import Staff,StaffBulkUpload, StaffDocument
from .forms import StaffForm, StaffDocumentUploadForm


class StaffListView(ListView,PermissionRequiredMessageMixin):
    model = Staff
    permission_required = 'staffs.view_staff'


class StaffDetailView(DetailView,PermissionRequiredMessageMixin):
    model = Staff
    permission_required = 'staffs.view_staff'
    template_name = "staffs/staff_detail.html"



class StaffCreateView(SuccessMessageMixin, PermissionRequiredMessageMixin, CreateView):
    model = Staff
    form_class = StaffForm
    permission_required = "staffs.add_staff"
    success_message = "New staff successfully added"

    def form_valid(self, form):
        response = super().form_valid(form)  # Save the Staff instance first

        files = self.request.FILES.getlist('documents')  # 'documents' comes from <input name="documents">
        for f in files:
            StaffDocument.objects.create(
                staff=self.object,    # the newly created staff
                document=f,
                title=f.name          # Optional: you can allow user to give custom title later
            )

        return response



class StaffUpdateView(SuccessMessageMixin,PermissionRequiredMessageMixin, UpdateView):
    model = Staff
    fields = "__all__"
    permission_required = "staffs.update_staff"
    success_message = "Record successfully updated."

    def get_form(self):
        """add date picker in forms"""
        form = super(StaffUpdateView, self).get_form()
        form.fields["date_of_birth"].widget = widgets.DateInput(attrs={"type": "date"})
        form.fields["date_of_joining"].widget = widgets.DateInput(
            attrs={"type": "date"}
        )
        form.fields["address"].widget = widgets.Textarea(attrs={"rows": 1})
        form.fields["others"].widget = widgets.Textarea(attrs={"rows": 1})
        return form


class StaffDeleteView(PermissionRequiredMessageMixin,DeleteView):
    model = Staff
    permission_required = "staffs.delete_staff"
    success_url = reverse_lazy("staff-list")


class StaffBulkUploadView(LoginRequiredMixin, SuccessMessageMixin,PermissionRequiredMessageMixin, CreateView):
    model = StaffBulkUpload
    template_name = "staffs/staff_upload.html"
    fields = ["csv_file"]
    success_url = "/staff/list"
    permission_required = 'staffs.add_staffbulkupload' 
    success_message = "Successfully uploaded staff"


class DownloadCSVViewdownloadcsv(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="staff_template.csv"'

        writer = csv.writer(response)
        writer.writerow(
            [
                "emp_code",
                "firstname",
                "surname",
                "gender",
                "date_of_birth",
                "date_of_joining",
                "adhar_card_number",
                "address",
                "mobile_number",
            ]
        )

        return response

class StaffDocumentUploadView(View):
    def get(self, request, staff_id):
        form = StaffDocumentUploadForm()
        return render(request, 'upload_documents.html', {'form': form, 'staff_id': staff_id})

    def post(self, request, staff_id):
        form = StaffDocumentUploadForm(request.POST, request.FILES)
        staff = Staff.objects.get(id=staff_id)

        files = request.FILES.getlist('documents')  # get multiple files

        if form.is_valid():
            for f in files:
                StaffDocument.objects.create(
                    staff=staff,
                    document=f,
                    title=f.name  # use filename as title, or customize
                )
            messages.success(request, "Documents uploaded successfully.")
            return redirect('staff_detail', staff_id=staff_id)  # redirect wherever you want

        return render(request, 'upload_documents.html', {'form': form, 'staff_id': staff_id})
