from django.contrib import admin
from .models import *


# Register your models here.
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    pass

@admin.register(StudentClass)
class StudentClassAdmin(admin.ModelAdmin):
    pass
    

    

