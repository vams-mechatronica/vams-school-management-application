from django import forms
from .models import Staff


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class StaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        exclude = ['user', 'current_status','staff_image'] 

    def __init__(self, *args, **kwargs):
        super(StaffForm, self).__init__(*args, **kwargs)
        self.fields["date_of_birth"].widget = forms.widgets.DateInput(attrs={"type": "date"})
        self.fields["date_of_joining"].widget = forms.widgets.DateInput(attrs={"type": "date"})
        self.fields["address"].widget = forms.widgets.Textarea(attrs={"rows": 1})
        self.fields["others"].widget = forms.widgets.Textarea(attrs={"rows": 1})
    

class StaffDocumentUploadForm(forms.Form):
    documents = forms.FileField(
        widget=MultipleFileInput(attrs={'multiple': True}),
        label="Upload Documents"
    )