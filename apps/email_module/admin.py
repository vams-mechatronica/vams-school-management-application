from django.contrib import admin
from .models import EmailTemplate, EmailSentLogs

# Register your models here.
@admin.register(EmailTemplate)
class EmailTemplateAdmin(admin.ModelAdmin):
    pass

@admin.register(EmailSentLogs)
class EmailSentLogsAdmin(admin.ModelAdmin):
    list_display = ('template_name','to_emails','sent_at')
    

    
