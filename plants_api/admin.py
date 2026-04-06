from django.contrib import admin
from .models import Plant, WateringHistory, CareRequirements

@admin.register(Plant)
class PlantAdmin(admin.ModelAdmin):
    list_display = ['name', 'type', 'owner', 'location', 'moisture', 'last_watered', 'created_at']
    list_filter = ['type', 'created_at', 'owner']
    search_fields = ['name', 'location']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(WateringHistory)
class WateringHistoryAdmin(admin.ModelAdmin):
    list_display = ['plant', 'watered_at', 'moisture_before', 'moisture_after']
    list_filter = ['watered_at', 'plant']
    search_fields = ['plant__name']
    readonly_fields = ['watered_at']

@admin.register(CareRequirements)
class CareRequirementsAdmin(admin.ModelAdmin):
    list_display = ['plant', 'water_frequency', 'light_requirement', 'temperature']
    search_fields = ['plant__name']
