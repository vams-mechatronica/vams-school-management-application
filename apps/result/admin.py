from django.contrib import admin
from .models import *
# Register your models here.
@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_filter = ('term',)
    
