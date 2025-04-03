from django.contrib import admin
from .models import *
# Register your models here.
@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('id','student','session','month','previous_balance','total_payable','status','updated_at')
    search_fields = ('student','month')
    

@admin.register(InvoiceItem)
class InvoiceItemAdmin(admin.ModelAdmin):
    list_display = ('id','invoice','description','amount')
    search_fields = ('invoice',)
    
@admin.register(Receipt)
class ReceiptAdmin(admin.ModelAdmin):
    list_display = ('id','invoice','amount_paid','payment_mode','date_paid')
    
