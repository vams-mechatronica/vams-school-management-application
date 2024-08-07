from django.contrib import admin
from .models import *
# Register your models here.
@admin.register(SiteConfig)
class SiteConfigAdmin(admin.ModelAdmin):
    pass
    
@admin.register(AcademicTerm)
class AcademicTermAdmin(admin.ModelAdmin):
    pass

@admin.register(AcademicSession)
class AcademicSessionAdmin(admin.ModelAdmin):
    pass

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    pass
    

    

    

