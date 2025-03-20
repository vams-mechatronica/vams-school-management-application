from django.contrib import admin
from .models import Staff, StaffBulkUpload


# Register your models here.
@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    pass

@admin.register(StaffBulkUpload)
class StaffBulkUploadAdmin(admin.ModelAdmin):
    pass
    

    
