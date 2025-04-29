from django.contrib import admin
from .models import Staff, StaffBulkUpload, StaffCategory, StaffDocument


# Register your models here.
@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    pass

@admin.register(StaffBulkUpload)
class StaffBulkUploadAdmin(admin.ModelAdmin):
    pass

@admin.register(StaffCategory)
class StaffCategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(StaffDocument)
class StaffDocumentAdmin(admin.ModelAdmin):
    pass
    


    

    

    
