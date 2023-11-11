from django.contrib import admin
from leaflet.admin import LeafletGeoAdmin
from .models import Location
# Register your models here.
@admin.register(Location)
class LocationAdmin(LeafletGeoAdmin):
    list_display = ['id','coordinates']