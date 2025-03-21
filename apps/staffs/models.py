from django.core.validators import RegexValidator
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
import os
from django.core.exceptions import ValidationError


class Staff(models.Model):
    STATUS = [(1, "Active"), (0, "Inactive")]

    GENDER = [("male", "Male"), ("female", "Female")]

    current_status = models.BooleanField(default=1,choices=STATUS)
    emp_code = models.CharField(max_length=200, unique=True,default=f"VAMS/emp/{timezone.now().year}/{timezone.now().strftime('%m%d%H%M%S')}")
    surname = models.CharField(max_length=200)
    firstname = models.CharField(max_length=200)
    other_name = models.CharField(max_length=200, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER, default="male")
    date_of_birth = models.DateField(default=timezone.now)
    date_of_joining = models.DateField(default=timezone.now)
    adhar_card_number = models.CharField(max_length=12, blank=True, null=True)

    mobile_num_regex = RegexValidator(
        regex="^[0-9]{10,15}$", message="Entered mobile number isn't in a right format!"
    )
    mobile_number = models.CharField(
        validators=[mobile_num_regex], max_length=13, blank=True
    )
    email = models.EmailField(_("Email Address"), max_length=254, null=True, blank=True)
    address = models.TextField(blank=True)
    others = models.TextField(blank=True)
    user = models.OneToOneField(User, on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return f"{self.surname} {self.firstname} {self.other_name}"

    def get_absolute_url(self):
        return reverse("staff-detail", kwargs={"pk": self.pk})
    
    def get_full_name(self):
        return f"{self.firstname} {self.surname}"

def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1].lower()
    allowed_extensions = [".csv", ".xlsx"]
    if ext not in allowed_extensions:
        raise ValidationError(_(f"Invalid file type: {ext}. Only CSV and XLSX files are allowed."))

class StaffBulkUpload(models.Model):
    date_uploaded = models.DateTimeField(auto_now=True)
    csv_file = models.FileField(upload_to="staff/bulkupload/", validators=[validate_file_extension])