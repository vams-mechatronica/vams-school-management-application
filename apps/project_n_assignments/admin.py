from django.contrib import admin
from .models import *


# Register your models here.
@admin.register(ClassAssignmentNProject)
class ClassAssignmentNProjectAdmin(admin.ModelAdmin):
    pass
    
