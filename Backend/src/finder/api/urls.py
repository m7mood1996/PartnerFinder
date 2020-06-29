from rest_framework import routers

from django.urls import path, include
from .views import OrganizationProfileViewSet, EventViewSet, ParticipantsViewSet, CallViewSet, \
    UpdateSettingsViewSet, AlertsSettingsViewSet, ScoresViewSet, AlertsB2match

router = routers.DefaultRouter()

router.register('organizations', OrganizationProfileViewSet)
router.register('', OrganizationProfileViewSet)
router.register('updates', UpdateSettingsViewSet)
router.register('alerts', AlertsSettingsViewSet)
router.register('calls', CallViewSet)

router.register('events', EventViewSet)
router.register('participants', ParticipantsViewSet)
router.register('scores', ScoresViewSet)
router.register("b2matchalerts", AlertsB2match)

urlpatterns = [
    path('', include(router.urls))
]
