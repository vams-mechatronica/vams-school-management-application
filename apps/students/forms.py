# forms.py
from django import forms
from .models import StudentClass, Student

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            'registration_number','sr_number','pen_number', 'firstname', 'other_name','surname',
            'father_name', 'mother_name', 'gender', 'date_of_birth', 'date_of_admission',
            'category','caste_category','current_class', 'adharcard_number', 'adharcard','parent_mobile_number','email',
            'number_of_siblings','select_siblings', 'address', 'others'
        ]

        # widgets = {
        #     'uses_transport': forms.CheckboxInput(attrs={
        #         'class': 'form-check-input ml-0'
        #     }),
        # }

    def __init__(self, *args, **kwargs):
        super(StudentForm, self).__init__(*args, **kwargs)
        # self.fields['uses_transport'].label = "Uses Transport"

class PromotionForm(forms.Form):
    current_class = forms.ModelChoiceField(queryset=StudentClass.objects.all(), label="Current Class:",widget=forms.Select(attrs={'class': 'form-select col-md-5'}))
    new_class = forms.ModelChoiceField(queryset=StudentClass.objects.all(), label="Promote To:",widget=forms.Select(attrs={'class': 'form-select col-md-3'}))
    students = forms.ModelMultipleChoiceField(
        queryset=Student.objects.none(),
        widget=forms.SelectMultiple(attrs={'class': 'form-control', 'size': '5'}),
        required=False,
        help_text='Hold down “Control”, or “Command” on a Mac, to select more than one.'
    )

    def __init__(self, *args, **kwargs):
        class_id = kwargs.pop('class_id', None)
        super(PromotionForm, self).__init__(*args, **kwargs)
        
        if class_id:
            self.fields['students'].queryset = Student.objects.filter(current_class_id=class_id)
