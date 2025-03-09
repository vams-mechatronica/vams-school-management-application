from django.contrib import admin
from .models import Driver, Vehicle, Route, Trip

admin.site.register(Driver)
admin.site.register(Vehicle)
admin.site.register(Route)
admin.site.register(Trip)
