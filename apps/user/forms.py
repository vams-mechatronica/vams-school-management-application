from django import forms
from django.contrib.auth import get_user_model
user = get_user_model()
from django.urls import reverse, reverse_lazy
from apps.attendance.models import Student, Staff, StudentAttendance, StaffAttendance

class UserForm(forms.ModelForm):

    class Meta:
        model = user
        fields = ('username','password')

class UserCreateForm(forms.ModelForm):
    student_or_staff = forms.ChoiceField(
        choices=[('admin', 'Admin'), ('student', 'Student'), ('staff', 'Staff')],
        label='Select Role',
        required=True,
        widget=forms.Select(attrs={'class': 'form-control', 'onchange': 'updateUserList(this)'})
    )

    selected_person = forms.ModelChoiceField(
        queryset=Student.objects.none(),
        label='Select User',
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = user
        fields = ['username', 'email', 'first_name', 'last_name', 'password']

    def __init__(self, *args, **kwargs):
        role = kwargs.pop('role', None)
        super(UserCreateForm, self).__init__(*args, **kwargs)
        self.fields['password'].widget = forms.PasswordInput()
        self.load_user_dropdown(role)

    def load_user_dropdown(self, role):
        """Dynamically populate user dropdown based on role."""
        if role == 'student':
            self.fields['selected_person'].queryset = Student.objects.filter(user__isnull=True)
        elif role == 'staff':
            self.fields['selected_person'].queryset = Staff.objects.filter(user__isnull=True)
        else:
            self.fields['selected_person'].queryset = Staff.objects.none()  # Admin has no related model
        
        self.order_fields(['student_or_staff', 'selected_person', 'username', 'email', 'first_name', 'last_name', 'password'])

    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data.get('selected_person'):
            raise forms.ValidationError("Please select a valid user.")
        return cleaned_data
