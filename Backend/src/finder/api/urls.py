from rest_framework import routers

from django.urls import path, include
from .views import OrganizationProfileViewSet

router = routers.DefaultRouter()
router.register('organizations', OrganizationProfileViewSet)

urlpatterns = [
    path('', include(router.urls))
]
