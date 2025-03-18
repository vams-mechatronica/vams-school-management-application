from django.core.validators import RegexValidator
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from apps.corecode.models import StudentClass
from apps.transport.models import Route
from django.utils.translation import gettext_lazy as _




class Student(models.Model):
    STATUS_CHOICES = [(1, "Active"), (0, "Inactive")]

    GENDER_CHOICES = [("male", "Male"), ("female", "Female")]

    current_status = models.BooleanField(default=1, choices=STATUS_CHOICES)
    registration_number = models.CharField(max_length=200, unique=True,help_text=f"VAMS/{timezone.now().year}/{timezone.now().strftime('%m')}/{timezone.now().strftime('%d')}/{timezone.now().strftime('%S')}")
    surname = models.CharField(max_length=200, blank=True,null=True)
    firstname = models.CharField(max_length=200)
    other_name = models.CharField(max_length=200, blank=True)
    father_name = models.CharField(max_length=500, blank=True,null=True)
    mother_name = models.CharField(max_length=500, blank=True,null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default="male")
    date_of_birth = models.DateField(default=timezone.now)
    date_of_admission = models.DateField(default=timezone.now)
    current_class = models.ForeignKey(
        StudentClass, on_delete=models.SET_NULL, blank=True, null=True
    )

    mobile_num_regex = RegexValidator(
        regex="^[0-9]{10,15}$", message="Entered mobile number isn't in a right format!"
    )
    adhar_num_validator = RegexValidator(
        regex="^[0-9]{12,12}$", message="Entered Adhar number isn't valid!"
    )
    parent_mobile_number = models.CharField(
        validators=[mobile_num_regex], max_length=13, blank=True
    )

    address = models.TextField(blank=True)
    others = models.TextField(blank=True)
    adharcard_number = models.CharField(
        validators=[adhar_num_validator], max_length=12, blank=True
    )
    adharcard = models.ImageField(blank=True, upload_to="students/adharcard/")
    user = models.OneToOneField(User, on_delete=models.SET_NULL, blank=True, null=True)

    uses_transport = models.BooleanField(default=False, help_text="Does the student use school transport?")
    route = models.ForeignKey(Route, on_delete=models.SET_NULL, null=True, blank=True, related_name="students")
    pickup_drop_location = models.CharField(max_length=255, blank=True, help_text="Pickup/Drop location for transport")
    pickup_time = models.TimeField(null=True, blank=True, help_text="Pickup time for the student")
    drop_time = models.TimeField(null=True, blank=True, help_text="Drop time for the student")

    email = models.EmailField(_("Email Address"), max_length=254, null=True, blank=True)


    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)

    class Meta:
        ordering = ["surname", "firstname", "other_name"]

    def __str__(self):
        return f"{self.surname} {self.firstname} {self.other_name} ({self.registration_number})"

    def get_absolute_url(self):
        return reverse("student-detail", kwargs={"pk": self.pk})
    
    def get_fullname(self):
        return "{firstname} {othername} {surname}".format(firstname=self.firstname,othername=self.other_name, surname=self.surname)


class StudentBulkUpload(models.Model):
    date_uploaded = models.DateTimeField(auto_now=True)
    csv_file = models.FileField(upload_to="students/bulkupload/")
