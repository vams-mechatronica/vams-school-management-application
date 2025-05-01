# forms.py
from django import forms
from .models import ClassAssignmentNProject

class ClassAssignmentNProjectForm(forms.ModelForm):
    
    class Meta:
        model = ClassAssignmentNProject
        exclude = ('user',)

