from rest_framework import routers

from django.urls import path, include
from .views import OrganizationProfileViewSet, EventViewSet, ParticipantsViewSet, CallViewSet, \
    UpdateSettingsViewSet, AlertsSettingsViewSet, ScoresViewSet

router = routers.DefaultRouter()
router.register('organizations', OrganizationProfileViewSet)
router.register('events', EventViewSet)
router.register('participants', ParticipantsViewSet)
router.register('genericSearch', OrganizationProfileViewSet)
router.register('calls', CallViewSet)
router.register('scores', ScoresViewSet)
router.register('updates', UpdateSettingsViewSet)
router.register('alerts', AlertsSettingsViewSet)

urlpatterns = [
    path('', include(router.urls))
]
