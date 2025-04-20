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

@admin.register(EmailMessageImageLink)
class EmailMessageImageLinkAdmin(admin.ModelAdmin):
    pass

@admin.register(ClassSubjectRelation)
class ClassSubjectRelationAdmin(admin.ModelAdmin):
    list_display = ('class_id','subject','created_at')
    search_fields = ('class_id','subject')
    ordering = ('class_id','subject')
    
@admin.register(Holiday)
class HolidayAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'created_at', 'updated_at')
    ordering = ('-date',)

    

    

    

