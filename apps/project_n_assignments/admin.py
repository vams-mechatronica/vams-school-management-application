from django.contrib import admin
from .models import *


# Register your models here.
@admin.register(ClassAssignmentNProject)
class ClassAssignmentNProjectAdmin(admin.ModelAdmin):
    pass

@admin.register(StudentAssignmentStatus)
class StudentAssignmentStatusAdmin(admin.ModelAdmin):
    list_display = ('assignment','student','is_submitted','submitted_at')
    

