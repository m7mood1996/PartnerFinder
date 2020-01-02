from rest_framework import routers

from django.urls import path
from .views import OrganizationProfileViewSet

router = routers.DefaultRouter()

router.register('',
                OrganizationProfileViewSet, 'finder')

urlpatterns = router.urls
