from django.contrib import admin
from .models import *
# Register your models here.
@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    pass
    

@admin.register(InvoiceItem)
class InvoiceItemAdmin(admin.ModelAdmin):
    pass
    
@admin.register(Receipt)
class ReceiptAdmin(admin.ModelAdmin):
    pass
    
