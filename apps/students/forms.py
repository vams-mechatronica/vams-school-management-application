# forms.py
from django import forms
from .models import StudentClass, Student

class PromotionForm(forms.Form):
    current_class = forms.ModelChoiceField(queryset=StudentClass.objects.all(), label="Current Class")
    new_class = forms.ModelChoiceField(queryset=StudentClass.objects.all(), label="Promote To")
    students = forms.ModelMultipleChoiceField(
        queryset=Student.objects.none(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    def __init__(self, *args, **kwargs):
        class_id = kwargs.pop('class_id', None)
        super(PromotionForm, self).__init__(*args, **kwargs)
        if class_id:
            self.fields['students'].queryset = Student.objects.filter(current_class_id=class_id)
