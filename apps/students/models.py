from django.core.validators import RegexValidator
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from apps.corecode.models import StudentClass
from apps.transport.models import Route
from django.utils.translation import gettext_lazy as _
import os
from django.core.exceptions import ValidationError




class Student(models.Model):
    STATUS_CHOICES = [(1, "Active"), (0, "Inactive")]

    GENDER_CHOICES = [("male", "Male"), ("female", "Female")]

    current_status = models.BooleanField(default=1, choices=STATUS_CHOICES)
    registration_number = models.CharField(max_length=200, unique=True,help_text=f"VAMS/{timezone.now().year}/{timezone.now().strftime('%m')}/{timezone.now().strftime('%d')}/{timezone.now().strftime('%S')}")
    surname = models.CharField(_("Last Name"),max_length=200, blank=True,null=True)
    firstname = models.CharField(_("First Name"),max_length=200)
    other_name = models.CharField(_("Middle Name"),max_length=200, blank=True)
    father_name = models.CharField(_("Father's Name"),max_length=500, blank=True,null=True)
    mother_name = models.CharField(_("Mother's Name"),max_length=500, blank=True,null=True)
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
    parent_mobile_number = models.CharField(_("Contact No."),
        validators=[mobile_num_regex], max_length=13, blank=True, help_text="Enter parent's mobile number."
    )

    address = models.TextField(blank=True)
    others = models.TextField(blank=True)
    adharcard_number = models.CharField(
        validators=[adhar_num_validator], max_length=12, blank=True, help_text="Enter 12 digit adharcard number"
    )
    adharcard = models.ImageField(blank=True, upload_to="students/adharcard/",help_text="Upload adharcard Image")
    student_image = models.ImageField(_("Student Image"), upload_to="students/profile_image/", null=True,blank=True)
    roll_number = models.IntegerField(_("Roll Number"),null=True,blank=True)
    user = models.OneToOneField(User, on_delete=models.SET_NULL, blank=True, null=True)

    uses_transport = models.BooleanField(default=False, help_text="Does the student use school transport?")
    route = models.ForeignKey(Route, on_delete=models.SET_NULL, null=True, blank=True, related_name="students")
    pickup_drop_location = models.CharField(max_length=255, blank=True, help_text="Pickup/Drop location for transport")
    pickup_time = models.TimeField(null=True, blank=True, help_text="Pickup time for the student")
    drop_time = models.TimeField(null=True, blank=True, help_text="Drop time for the student")

    email = models.EmailField(_("Email Address"), max_length=254, null=True, blank=True)
    number_of_siblings = models.IntegerField(_("Number of Siblings"),default=0,help_text="Number of siblings studying in this school (including this student)")
    select_siblings = models.ManyToManyField("self", verbose_name=_("Select Siblings"), null=True, blank=True,help_text="Press Hold down “Control”, or “Command” on a Mac, to select more than one.")


    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)

    class Meta:
        ordering = ["surname", "firstname", "other_name"]
        permissions = [
            ("can_promote_students", "Can promote students to next class"),
        ]

    def __str__(self):
        return f"{self.surname if self.surname else '-'} {self.firstname} - F: {self.father_name} ({self.registration_number})"

    def get_absolute_url(self):
        return reverse("student-detail", kwargs={"pk": self.pk})
    
    def get_fullname(self):
        return f"{self.firstname or '-'} {self.surname or '-'}"

    def get_sibling_names(self):
        siblings = self.select_siblings.all()
        names = [f"{sibling.firstname} {sibling.surname or '-'}" for sibling in siblings]
        return ", ".join(names)

    def clean(self):
        if self.roll_number is not None:
            if Student.objects.exclude(pk=self.pk).filter(roll_number=self.roll_number).exists():
                raise ValidationError({'roll_number': 'This roll number is already in use.'})

def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1].lower()
    allowed_extensions = [".csv", ".xlsx"]
    if ext not in allowed_extensions:
        raise ValidationError(_(f"Invalid file type: {ext}. Only CSV and XLSX files are allowed."))

class StudentBulkUpload(models.Model):
    date_uploaded = models.DateTimeField(auto_now=True)
    csv_file = models.FileField(upload_to="students/bulkupload/", validators=[validate_file_extension])


