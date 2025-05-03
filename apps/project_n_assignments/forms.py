# forms.py
from django import forms
from .models import ClassAssignmentNProject, Student

class ClassAssignmentNProjectForm(forms.ModelForm):
    class Meta:
        model = ClassAssignmentNProject
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['students'].queryset = Student.objects.none()

        if 'for_class' in self.data:
            try:
                class_id = int(self.data.get('for_class'))
                self.fields['students'].queryset = Student.objects.filter(student_class_id=class_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk and self.instance.for_class:
            self.fields['students'].queryset = Student.objects.filter(student_class=self.instance.for_class)


