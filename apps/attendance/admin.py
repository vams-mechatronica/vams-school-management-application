from django.contrib import admin
from .models import StaffAttendance, StudentAttendance, StaffLeaveRequest


# Register your models here.
@admin.register(StudentAttendance)
class StudentAttendanceAdmin(admin.ModelAdmin):
    pass

@admin.register(StaffAttendance)
class StaffAttendanceAdmin(admin.ModelAdmin):
    pass

@admin.register(StaffLeaveRequest)
class LeaveRequestAdmin(admin.ModelAdmin):
    list_display = ('staff', 'start_date', 'end_date', 'status', 'submitted_at')
    list_filter = ('status',)

    
