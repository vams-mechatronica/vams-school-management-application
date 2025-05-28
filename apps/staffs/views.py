from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.forms import widgets
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from apps.email_module.modules import send_html_email_async
from django.utils import timezone
from apps.corecode.models import SchoolDetail
import csv
from django.contrib.auth.models import User, Group
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView,View
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from apps.result.utils import PermissionRequiredMessageMixin
from .models import Staff,StaffBulkUpload, StaffDocument
from .forms import StaffForm, StaffDocumentUploadForm


class StaffListView(PermissionRequiredMessageMixin,LoginRequiredMixin,ListView):
    model = Staff
    permission_required = 'staffs.view_staff'


class StaffDetailView(PermissionRequiredMessageMixin,LoginRequiredMixin,DetailView):
    model = Staff
    permission_required = 'staffs.view_staff'
    template_name = "staffs/staff_detail.html"



class StaffCreateView(PermissionRequiredMessageMixin,LoginRequiredMixin,SuccessMessageMixin, CreateView):
    model = Staff
    form_class = StaffForm
    permission_required = "staffs.add_staff"
    success_message = "New staff successfully added"

    def __init__(self, **kwargs):
        self.school_details = SchoolDetail.objects.latest('updated_at')

    def get_registration_number(self):
        try:
            last_staff = Staff.objects.latest('updated_at')
            last_id = last_staff.id
        except Staff.DoesNotExist:
            import random
            last_id = random.randint(0, 99999)

        try:
            school_short_name = self.school_details.short_name
        except SchoolDetail.DoesNotExist:
            school_short_name = "VAMS"

        timestamp = timezone.now().strftime('%d')
        reg_number = f"{school_short_name}/Emp/{timezone.now().year}/{timezone.now().month}/{timestamp}/{last_id + 1}"
        return reg_number
    
    def check_if_user_exists(self, username):
        try:
            user = User.objects.get(username=username)
            return True
        except User.DoesNotExist:
            return False

    def form_valid(self, form):
        response = super().form_valid(form)
        staff = form.instance

        files = self.request.FILES.getlist('documents')
        for f in files:
            StaffDocument.objects.create(
                staff=self.object, 
                document=f,
                title=f.name    
            )
        
        if not staff.emp_code:
            staff.emp_code = self.get_registration_number()

        firstname = staff.firstname.strip().lower()
        lastname = staff.surname.strip().lower()
        # serial_number = student.registration_number.split('/')[-1]
        username = f"{lastname}.{firstname}"
        user_exists = self.check_if_user_exists(username=username)
        if user_exists:
            username = username + "".join(staff.emp_code.split('/')[-3:-1])

        # Generate password
        dob_part = staff.date_of_birth.strftime("%d%m")
        today_part = timezone.now().strftime("%d%m%Y")
        password = f"{dob_part}{firstname}{lastname}{today_part}#"

        # Create or get user
        if staff.email:
            user, created = User.objects.get_or_create(username=username,email=staff.email, defaults={
                "first_name": staff.firstname,
                "last_name": staff.surname,
            })
        else:
            user, created = User.objects.get_or_create(username=username, defaults={
                "first_name": staff.firstname,
                "last_name": staff.surname,
            })

        if created:
            user.set_password(password)
            user.save()
        
        # Assign to Student group
        student_group, _ = Group.objects.get_or_create(name="staff")
        user.groups.add(student_group)

        # Assign user and registration number to student
        staff.user = user
        
        if staff.email:
            # send congratulation email
            send_html_email_async(template_name="new_staff_enrollment_congratulation",
                                to_emails=[staff.email],content_context={
                "student_name": staff.get_fullname(),
                "registration_number":staff.emp_code,
                "current_year":timezone.now().year,
                "sitename": self.school_details.name,
                "username":staff.user.username,
                "password":password
            })

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
                "pancard_number"
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
                    title=f.name
                )
            messages.success(request, "Documents uploaded successfully.")
            return redirect('staff_detail', staff_id=staff_id)  # redirect wherever you want

        return render(request, 'upload_documents.html', {'form': form, 'staff_id': staff_id})
