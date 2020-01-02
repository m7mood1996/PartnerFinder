from rest_framework import routers

from django.urls import path
from .views import OrganizationProfileViewSet

router = routers.DefaultRouter()

router.register('api/OrganizationProfiles',
                OrganizationProfileViewSet, 'finder')

urlpatterns = router.urls
# urlpatterns = [
#     path('',OrganizationProfileViewSet.as_view())
# ]
