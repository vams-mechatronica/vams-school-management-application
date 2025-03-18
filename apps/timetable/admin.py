from django.contrib import admin
from .models import Timetable, PeriodDay,Period


admin.site.register(Timetable)
@admin.register(Period)
class PeriodAdmin(admin.ModelAdmin):
    pass

@admin.register(PeriodDay)
class PeriodDayAdmin(admin.ModelAdmin):
    pass
    

    

