from django.core.validators import RegexValidator
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from apps.corecode.models import FeeCategory, StudentClass
from apps.transport.models import Route
from django.utils.translation import gettext_lazy as _
import os
from django.core.exceptions import ValidationError

class Category(models.Model):
    name = models.CharField(_("Category"), max_length=50)

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categorys")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Category_detail", kwargs={"pk": self.pk})

class CasteCategory(models.Model):
    name = models.CharField(_("Caste"), max_length=500)
    parent_category = models.ForeignKey(Category, verbose_name=_("Parent Category"), on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("CasteCategory")
        verbose_name_plural = _("CasteCategorys")

    def __str__(self):
        return "c: {} pc: {}".format(self.name, self.parent_category)

    def get_absolute_url(self):
        return reverse("CasteCategory_detail", kwargs={"pk": self.pk})

class Student(models.Model):
    STATUS_CHOICES = [(1, "Active"), (0, "Inactive")]
    GENDER_CHOICES = [("male", "Male"), ("female", "Female")]
    # CATEGORY_CHOICES = [(0,"General"),(1,"Other Backward Classes (OBC)"),(2,"Scheduled Caste (SC)"),(3, "Scheduled Tribes (ST)"),(4,"Economically Weaker Sections (EWS)"),(5,"Persons with Benchmark Disabilities (PwBD)")]

    current_status = models.BooleanField(default=1, choices=STATUS_CHOICES)
    registration_number = models.CharField(max_length=200, unique=True,help_text=f"VAMS/{timezone.now().year}/{timezone.now().strftime('%m')}/{timezone.now().strftime('%d')}/{timezone.now().strftime('%S')}")
    sr_number = models.CharField(_("SR Number"), max_length=100, null=True, blank=True, help_text="Please enter SR number")
    pen_number = models.CharField(_("PEN Number"), max_length=100, null=True, blank=True, help_text="Please enter PEN number")
    surname = models.CharField(_("Last Name"),max_length=200, blank=True,null=True)
    firstname = models.CharField(_("First Name"),max_length=200)
    other_name = models.CharField(_("Middle Name"),max_length=200, blank=True)
    father_name = models.CharField(_("Father's Name"),max_length=500, blank=True,null=True)
    mother_name = models.CharField(_("Mother's Name"),max_length=500, blank=True,null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default="male")
    category = models.ForeignKey(Category, verbose_name=_("Category"), on_delete=models.CASCADE, null=True, blank=True)
    caste_category = models.ForeignKey(CasteCategory, verbose_name=_("Caste"), on_delete=models.CASCADE, null=True, blank=True)
    fee_category = models.ForeignKey(FeeCategory, verbose_name=_("Fee Category"), on_delete=models.SET_NULL, null=True, blank=True)
    date_of_birth = models.DateField(default=timezone.now)
    date_of_admission = models.DateField(default=timezone.now)
    current_class = models.ForeignKey(
        StudentClass, on_delete=models.CASCADE,
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

    uses_transport = models.BooleanField(verbose_name=_("School Transport"),default=False, help_text="Does the student use school transport?")
    route = models.ForeignKey(Route, on_delete=models.SET_NULL, null=True, blank=True, related_name="students")
    pickup_drop_location = models.CharField(max_length=255, blank=True, help_text="Pickup/Drop location for transport")
    pickup_time = models.TimeField(null=True, blank=True, help_text="Pickup time for the student")
    drop_time = models.TimeField(null=True, blank=True, help_text="Drop time for the student")

    email = models.EmailField(_("Email Address"), max_length=254, null=True, blank=True)
    number_of_siblings = models.IntegerField(_("Number of Siblings"),default=0,help_text="Number of siblings studying in this school (including this student)")
    select_siblings = models.ManyToManyField("self", verbose_name=_("Select Siblings"), null=True, blank=True,help_text="Press Hold down “Control”, or “Command” on a Mac, to select more than one.")

    # ------ Previous school information
    name_of_previous_school = models.CharField(_("Name of Previous School"), max_length=500, null=True, blank=True)
    last_class_attended = models.ForeignKey(StudentClass, verbose_name=_("Last Class Attended"), on_delete=models.SET_NULL, null=True, blank=True, related_name="last_class")
    medium_of_instruction = models.CharField(_("Medium"), max_length=50, choices=((0,'English'),(0,'Hindi')),default=0)
    reason_of_leaving = models.TextField(_("Reason of Leaving"), null=True, blank=True)

    # ------ Emergency contact
    name = models.CharField(_("Name"), max_length=500, null=True, blank=True)
    relation_with_student = models.CharField(_("Relation with student"), max_length=500, null=True, blank=True)
    emergency_contact_number = models.CharField(_("Contact No."),
        validators=[mobile_num_regex], max_length=13, blank=True, help_text="Enter emergency contact number"
    )

    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)

    class Meta:
        ordering = ["surname", "firstname", "other_name"]
        permissions = [
            ("can_promote_students", "Can promote students to next class"),
        ]

    def __str__(self):
        return f"{self.surname if self.surname else '-'} {self.firstname} - F: {self.father_name} (Class: {self.current_class.name} - Reg: {self.registration_number })"

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


