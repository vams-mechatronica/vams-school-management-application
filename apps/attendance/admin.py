from django.contrib import admin
from .models import StaffAttendance, StudentAttendance


# Register your models here.
@admin.register(StudentAttendance)
class StudentAttendanceAdmin(admin.ModelAdmin):
    pass

@admin.register(StaffAttendance)
class StaffAttendanceAdmin(admin.ModelAdmin):
    pass
    

    
