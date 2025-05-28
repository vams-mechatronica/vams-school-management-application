# forms.py
from django import forms
from .models import ClassAssignmentNProject, Student
from django.core.exceptions import ValidationError


class ClassAssignmentNProjectForm(forms.ModelForm):
    class Meta:
        model = ClassAssignmentNProject
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['students'].queryset = Student.objects.none()
        self.fields['students'].required = False

        if 'for_class' in self.data:
            try:
                class_id = int(self.data.get('for_class'))
                self.fields['students'].queryset = Student.objects.filter(current_class_id=class_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk and self.instance.for_class:
            self.fields['students'].queryset = Student.objects.filter(current_class=self.instance.for_class)

    def clean(self):
        cleaned_data = super().clean()
        is_all = cleaned_data.get("is_assignment_for_all")
        students = cleaned_data.get("students")

        if not is_all and not students:
            raise ValidationError("You must select at least one student if 'All Students' is unchecked.")

        return cleaned_data


