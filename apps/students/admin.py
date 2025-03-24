from django.contrib import admin
from .models import *


# Register your models here.
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('id','firstname','surname','current_class','registration_number','created_at')

@admin.register(StudentClass)
class StudentClassAdmin(admin.ModelAdmin):
    list_display = ('id','name','tuition_fees','computer_fees','admission_fees','exam_fees','miscellaneous')
    search_fields = ('id','name')
    ordering = ('id','name','tuition_fees')

@admin.register(StudentBulkUpload)
class StudentBulkUploadAdmin(admin.ModelAdmin):
    list_display = ('id','date_uploaded','csv_file')
    

    

    

