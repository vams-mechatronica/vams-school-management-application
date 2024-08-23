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
        choices=[('admin','Admin'),('student', 'Student'), ('staff', 'Staff')],
        label='Select Role',
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    selected_person = forms.ChoiceField(
        label='Select User',
        required=True,
        widget=forms.Select(attrs={'class': 'form-control', 'data-url': reverse_lazy('get_users_list')})
    )

    class Meta:
        model = user
        fields = ['username', 'first_name', 'last_name', 'password']

    def __init__(self, *args, **kwargs):
        super(UserCreateForm, self).__init__(*args, **kwargs)
        self.fields['password'].widget = forms.PasswordInput()
        self.load_user_dropdown(role='student')

    def load_user_dropdown(self, role):
        if role == 'student':
            users = Student.objects.all()
        else:
            users = Staff.objects.all()

        choices = [(user.id, f" {user.surname} {user.firstname} {user.other_name} ({user.registration_number})") for user in users]
        self.fields['selected_person'].choices = choices