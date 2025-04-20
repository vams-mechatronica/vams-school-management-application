from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.urls import reverse,reverse_lazy
from django.utils.translation import gettext_lazy as _
# Create your models here.


class SiteConfig(models.Model):
    """Site Configurations"""

    key = models.SlugField()
    value = models.CharField(max_length=200)

    def __str__(self):
        return self.key



# Custom validator for file size
def validate_file_size(value):
    max_size = 5 * 1024 * 1024  # 5MB
    if value.size > max_size:
        raise ValidationError(_("File size must not exceed 5MB."))

# Allowed file extensions
ALLOWED_EXTENSIONS = ("jpg", "jpeg", "png")
FAVICON_ICON_ALLOWED_EXTENSION = ("ico",)

class SchoolDetail(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name="School Name",default="My School")
    short_name = models.CharField(max_length=50, unique=True, verbose_name="School Short Name",default="VAMS")
    slogan = models.CharField(max_length=255, blank=True, null=True, verbose_name="School Slogan")
    address = models.TextField(verbose_name="School Address")
    fee_collection = models.IntegerField(_("Fee Collection Type"),choices=[(0,'Monthly'),(1,'Quaterly'),(2,'Half Yearly'),(3,'Yearly')],default=0)

    # Image fields with validation
    logo_vertical = models.ImageField(
        upload_to="school/logos/", blank=True, null=True, verbose_name="Vertical Logo",
        validators=[FileExtensionValidator(ALLOWED_EXTENSIONS), validate_file_size]
    )
    logo_horizontal = models.ImageField(
        upload_to="school/logos/", blank=True, null=True, verbose_name="Horizontal Logo",
        validators=[FileExtensionValidator(ALLOWED_EXTENSIONS), validate_file_size]
    )
    favicon = models.ImageField(
        upload_to="school/favicon/", blank=True, null=True, verbose_name="Favicon Icon",
        validators=[FileExtensionValidator(FAVICON_ICON_ALLOWED_EXTENSION), validate_file_size]
    )
    letterhead = models.ImageField(
        upload_to="school/letterhead/", blank=True, null=True, verbose_name="Letterhead Image",
        validators=[FileExtensionValidator(ALLOWED_EXTENSIONS), validate_file_size]
    )
    signature = models.ImageField(
        upload_to="school/signatures/", blank=True, null=True, verbose_name="Signature Image",
        validators=[FileExtensionValidator(ALLOWED_EXTENSIONS), validate_file_size]
    )
    background_image = models.ImageField(
        upload_to="school/backgrounds/", blank=True, null=True, verbose_name="First Page Background",
        validators=[FileExtensionValidator(ALLOWED_EXTENSIONS), validate_file_size]
    )

    # Other details
    authorized_signatory = models.CharField(max_length=100, blank=True, null=True, verbose_name="Authorized Signatory")
    school_strength = models.PositiveIntegerField(default=0, verbose_name="School Strength")
    
    medium_choices = [
        ('English', 'English'),
        ('Hindi', 'Hindi'),
    ]
    medium = models.CharField(max_length=10, choices=medium_choices, verbose_name="Medium of Instruction")

    # Subdomain for multi-school support
    subdomain = models.CharField(max_length=100, unique=True, verbose_name="School Subdomain")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("SchoolDetail")
        verbose_name_plural = _("SchoolDetails")
    
    def save(self, *args, **kwargs):
        """Ensure only one instance of SchoolDetail exists."""
        if not self.pk and SchoolDetail.objects.exists():
            raise ValidationError("Only one SchoolDetail instance is allowed.")
        return super().save(*args, **kwargs)


class AcademicSession(models.Model):
    """Academic Session"""

    name = models.CharField(max_length=200, unique=True)
    current = models.BooleanField(default=True)
    start_date = models.DateField(_("Start Date"), auto_now=False, auto_now_add=False)
    end_date = models.DateField(_("End Date"), auto_now=False, auto_now_add=False)
    created_at = models.DateTimeField(_("Created at"), auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True, auto_now_add=False)

    class Meta:
        ordering = ["-name"]

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if self.current:
            AcademicSession.objects.filter(current=True).update(current=False)
        super().save(*args, **kwargs)


class AcademicTerm(models.Model):
    """Academic Term"""

    name = models.CharField(max_length=20, unique=True)
    current = models.BooleanField(default=True)
    start_date = models.DateField(_("Start Date"), auto_now=False, auto_now_add=False)
    end_date = models.DateField(_("End Date"), auto_now=False, auto_now_add=False)
    created_at = models.DateTimeField(_("Created at"), auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True, auto_now_add=False)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if self.current:
            AcademicTerm.objects.filter(current=True).update(current=False)
        super().save(*args, **kwargs)
    



class Subject(models.Model):
    """Subject"""

    name = models.CharField(max_length=200, unique=True)
    test_max_marks = models.IntegerField(_("Test Maximum Marks"),default=50)
    exam_max_marks = models.IntegerField(_("Exam Maximum Marks"),default=100)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class StudentClass(models.Model):
    name = models.CharField(max_length=200, unique=True)
    tuition_fees = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    computer_fees = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    admission_fees = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    exam_fees = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    miscellaneous = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    class Meta:
        verbose_name = "Class"
        verbose_name_plural = "Classes"
        ordering = ["name"]

    def __str__(self):
        return self.name

class ClassSubjectRelation(models.Model):
    class_id = models.ForeignKey(StudentClass, verbose_name=_("Class"), on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, verbose_name=_("Subjects"), on_delete=models.SET_NULL,null=True,blank=True)
    created_at = models.DateTimeField(_("Created at"), auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True, auto_now_add=False)
    
    class Meta:
        verbose_name = _("ClassSubjectRelation")
        verbose_name_plural = _("ClassSubjectRelations")

    def __str__(self):
        return "Class: {} Subject: {}".format(self.class_id,self.subject)

    def get_absolute_url(self):
        return reverse("ClassSubjectRelation_detail", kwargs={"pk": self.pk})



class EmailMessageImageLink(models.Model):
    image_1 = models.ImageField(upload_to='email/images/',blank=True,null=True)
    image_2 = models.ImageField(upload_to='email/images/',blank=True,null=True)
    image_3 = models.ImageField(upload_to='email/images/',blank=True,null=True)
    image_4 = models.ImageField(upload_to='email/images/',blank=True,null=True)
    image_5 = models.ImageField(upload_to='email/images/',blank=True,null=True)
    image_6 = models.ImageField(upload_to='email/images/',blank=True,null=True)
    image_7 = models.ImageField(upload_to='email/images/',blank=True,null=True)
    image_8 = models.ImageField(upload_to='email/images/',blank=True,null=True)
    image_9 = models.ImageField(upload_to='email/images/',blank=True,null=True)
    image_10 = models.ImageField(upload_to='email/images/',blank=True,null=True)
    image_11 = models.ImageField(upload_to='email/images/',blank=True,null=True)
    image_12 = models.ImageField(upload_to='email/images/',blank=True,null=True)
    image_13 = models.ImageField(upload_to='email/images/',blank=True,null=True)
    image_14 = models.ImageField(upload_to='email/images/',blank=True,null=True)
    image_15 = models.ImageField(upload_to='email/images/',blank=True,null=True)
    image_16 = models.ImageField(upload_to='email/images/',blank=True,null=True)
    image_17 = models.ImageField(upload_to='email/images/',blank=True,null=True)
    image_18 = models.ImageField(upload_to='email/images/',blank=True,null=True)
    image_19 = models.ImageField(upload_to='email/images/',blank=True,null=True)
    image_20 = models.ImageField(upload_to='email/images/',blank=True,null=True)

    class Meta:
        verbose_name = _("EmailMessageImageLink")
        verbose_name_plural = _("EmailMessageImageLinks")

    def __str__(self):
        return self.pk

class Holiday(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.date}"