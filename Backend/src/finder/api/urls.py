from rest_framework import routers

from django.urls import path, include
from .views import OrganizationProfileViewSet, EventViewSet, ParticipantsViewSet

router = routers.DefaultRouter()
router.register('organizations', OrganizationProfileViewSet)
router.register('events', EventViewSet)
router.register('participants', ParticipantsViewSet)
router.register('genericSearch', OrganizationProfileViewSet)
router.register('Calls', CallViewSet)

urlpatterns = [
    path('', include(router.urls))
]
