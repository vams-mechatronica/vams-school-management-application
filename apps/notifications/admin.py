from django.contrib import admin
from .models import *


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    pass

@admin.register(DeliveredNotification)
class DeliveredNotificationAdmin(admin.ModelAdmin):
    pass
    

    


# Register your models here.
