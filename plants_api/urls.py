from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet, PlantViewSet, WateringHistoryViewSet,
    SystemSettingsViewSet, PlantTypeViewSet, LocationViewSet,
    WateringScheduleViewSet, AutomationRuleViewSet
)

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'plants', PlantViewSet, basename='plant')
router.register(r'watering-history', WateringHistoryViewSet, basename='watering-history')
router.register(r'settings', SystemSettingsViewSet, basename='settings')
router.register(r'plant-types', PlantTypeViewSet, basename='plant-type')
router.register(r'locations', LocationViewSet, basename='location')
router.register(r'watering-schedules', WateringScheduleViewSet, basename='watering-schedule')
router.register(r'automation-rules', AutomationRuleViewSet, basename='automation-rule')

urlpatterns = [
    path('', include(router.urls)),
]
