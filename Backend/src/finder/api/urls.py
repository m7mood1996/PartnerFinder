from rest_framework import routers

from django.urls import path, include
from .views import OrganizationProfileViewSet, EventViewSet, ParticipantsViewSet

router = routers.DefaultRouter()
router.register('organizations', OrganizationProfileViewSet)
router.register('events', EventViewSet)
router.register('participants', ParticipantsViewSet)



urlpatterns = [
    path('', include(router.urls))
]
