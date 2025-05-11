from django import forms
from .models import Staff, StaffAttendance, StaffLeaveRequest
from datetime import date

class StaffAttendanceForm(forms.ModelForm):
    class Meta:
        model = StaffAttendance
        fields = ['status', 'time_in', 'time_out']
        widgets = {
            'time_in': forms.TimeInput(attrs={'type': 'time'}),
            'time_out': forms.TimeInput(attrs={'type': 'time'}),
        }

class BulkAttendanceForm(forms.Form):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), initial=date.today)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        staff_members = Staff.objects.all()
        for staff in staff_members:
            self.fields[f'attendance_{staff.id}'] = forms.ChoiceField(
                choices=StaffAttendance.ATTENDANCE_CHOICE, 
                label=f"{staff.get_full_name()}",
                required=False
            )
            self.fields[f'time_in_{staff.id}'] = forms.TimeField(
                required=False, widget=forms.TimeInput(attrs={'type': 'time'})
            )
            self.fields[f'time_out_{staff.id}'] = forms.TimeField(
                required=False, widget=forms.TimeInput(attrs={'type': 'time'})
            )


class LeaveRequestForm(forms.ModelForm):
    num_days = forms.IntegerField(label='Number of Days', required=False, disabled=True)
    class Meta:
        model = StaffLeaveRequest
        fields = ['start_date', 'end_date', 'reason']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'reason': forms.Textarea(attrs={'rows': 3}),
        }