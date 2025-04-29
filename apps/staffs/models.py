from django.core.validators import RegexValidator
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
import os
from django.core.exceptions import ValidationError
from apps.corecode.models import Subject, StudentClass

class StaffCategory(models.Model):

    name = models.CharField(_("Category Name"), max_length=50)
    class Meta:
        verbose_name = _("StaffCategory")
        verbose_name_plural = _("StaffCategorys")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("StaffCategory_detail", kwargs={"pk": self.pk})


class Staff(models.Model):
    STATUS = [(1, "Active"), (0, "Inactive")]

    GENDER = [("male", "Male"), ("female", "Female")]

    current_status = models.BooleanField(default=1,choices=STATUS)
    emp_code = models.CharField(max_length=200, unique=True,default=f"VAMS/emp/{timezone.now().year}/{timezone.now().strftime('%m%d%H%M%S')}")
    staff_category = models.ForeignKey(StaffCategory, verbose_name=_("Staff Category"), on_delete=models.SET_NULL,null=True,blank=True, help_text="Select Staff Category e.g. Teaching Staff, Helping Staff")
    firstname = models.CharField(max_length=200, verbose_name=_("First Name"))
    surname = models.CharField(max_length=200, verbose_name=_("Last Name"))
    other_name = models.CharField(max_length=200, blank=True, verbose_name=_("Middle Name"))
    gender = models.CharField(max_length=10, choices=GENDER, default="male")
    date_of_birth = models.DateField(default=timezone.now)
    date_of_joining = models.DateField(default=timezone.now)
    class_incharge = models.ForeignKey(StudentClass, verbose_name=_("Class Incharge"), on_delete=models.SET_NULL, null=True, blank=True, help_text="If staff is a class incharge of any class, select a class.")
    subject_expert = models.ManyToManyField(Subject, verbose_name=_("Subjects"),help_text="Select as many subjects which can be taught by this staff.")
    adhar_card_number = models.CharField(max_length=12, verbose_name=_("Adharcard Number"), blank=True, null=True, help_text="Enter 12digit adharcard number.")
    pancard_number = models.CharField(max_length=12, verbose_name=_("Pancard Number"), blank=True, null=True, help_text="Enter PAN Card number.")

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


class StaffDocument(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name='documents')
    document = models.FileField(upload_to='staff_documents/')
    title = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)