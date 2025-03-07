from django.contrib import admin
from .models import APKVersion

# Register your models here.
@admin.register(APKVersion)
class APKVersionAdmin(admin.ModelAdmin):
    list_display = ('os','version','uploaded_at')
    
