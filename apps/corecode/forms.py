from django import forms
from django.forms import ModelForm, modelformset_factory

from .models import (
    AcademicSession,
    AcademicTerm,
    SiteConfig,
    StudentClass,
    Subject,SchoolDetail,Holiday
)

SiteConfigForm = modelformset_factory(
    SiteConfig,
    fields=(
        "key",
        "value",
    ),
    extra=0,
)

from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator

# Allowed file extensions
ALLOWED_EXTENSIONS = ["jpg", "jpeg", "png", "ico"]

# Max file size (in bytes) → 5MB
MAX_FILE_SIZE = 5 * 1024 * 1024  

def validate_file_extension(value):
    """Ensure the uploaded file has a valid extension."""
    ext = value.name.split(".")[-1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise ValidationError(f"Unsupported file extension: {ext}. Allowed: {', '.join(ALLOWED_EXTENSIONS)}")

def validate_file_size(value):
    """Ensure the uploaded file does not exceed the max size."""
    if value.size > MAX_FILE_SIZE:
        raise ValidationError(f"File size exceeds the limit of 5MB. Your file is {value.size / (1024 * 1024):.2f}MB")

class SchoolDetailForm(forms.ModelForm):
    """Form for School Details with image validation."""

    class Meta:
        model = SchoolDetail
        fields = '__all__'

    def clean_logo_vertical(self):
        file = self.cleaned_data.get("logo_vertical")
        if file:
            validate_file_extension(file)
            validate_file_size(file)
        return file

    def clean_logo_horizontal(self):
        file = self.cleaned_data.get("logo_horizontal")
        if file:
            validate_file_extension(file)
            validate_file_size(file)
        return file

    def clean_favicon(self):
        file = self.cleaned_data.get("favicon")
        if file:
            validate_file_extension(file)
            validate_file_size(file)
        return file

    def clean_letterhead(self):
        file = self.cleaned_data.get("letterhead")
        if file:
            validate_file_extension(file)
            validate_file_size(file)
        return file

    def clean_signature(self):
        file = self.cleaned_data.get("signature")
        if file:
            validate_file_extension(file)
            validate_file_size(file)
        return file

    def clean_background_image(self):
        file = self.cleaned_data.get("background_image")
        if file:
            validate_file_extension(file)
            validate_file_size(file)
        return file


class AcademicSessionForm(ModelForm):
    prefix = "Academic Session"

    class Meta:
        model = AcademicSession
        fields = ["name", "current"]


class AcademicTermForm(ModelForm):
    prefix = "Academic Term"

    class Meta:
        model = AcademicTerm
        fields = ["name", "current"]


class SubjectForm(ModelForm):
    prefix = "Subject"

    class Meta:
        model = Subject
        fields = '__all__'


class StudentClassForm(ModelForm):
    prefix = "Class"

    class Meta:
        model = StudentClass
        fields = '__all__'


class CurrentSessionForm(forms.Form):
    current_session = forms.ModelChoiceField(
        queryset=AcademicSession.objects.all(),
        help_text='Click <a href="/session/create/?next=current-session/">here</a> to add new session',
    )
    current_term = forms.ModelChoiceField(
        queryset=AcademicTerm.objects.all(),
        help_text='Click <a href="/term/create/?next=current-session/">here</a> to add new term',
    )



class HolidaysForm(ModelForm):
    prefix = "Holiday"

    class Meta:
        model = Holiday
        fields = '__all__'