from django.contrib import admin
from .models import *
# Register your models here.
@admin.register(SiteConfig)
class SiteConfigAdmin(admin.ModelAdmin):
    pass
    
